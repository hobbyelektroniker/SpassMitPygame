import os
import math
import random
import pathlib

class Record:
    """
    0.1.0 22.07.2023
    Diese Klasse implementiert einen einfachen Recordtyp mit vordefinierten Feldern.
    Jedem Feld kann ein Standardwert zugeordnet werden.
    Die Struktur kann mit print() und repr() sinnvoll ausgelesen werden.
    repr() kann mit eval zur Erzeugung einer Kopie verwendet werden.

    Der Record kann mit .as_dict() auch als Dictionary ausgegeben werden. Es handelt sich dabei um dieselbe Instanz.
    Um eine unabhängige Kopie zu erhalten, muss .as_dict().copy() verwendet werden!

    Da es sich um eine normale Klasse mit Atrributen handelt,
    können weitere Felder nachträglich einfach hinzugefügt werden.

    Feldnamen ohne Vorgabenwerte können mit dem Wert None oder als String angegeben werden.

    r = Record('a', b=None, c='C', d=5)

    Ein Record kann auch mit Record.from_dict(d) aus einem Dictionary erzeugt werden. Der Record und
    das Dictionary bleiben dabei gekoppelt. Auch hier können die Instanzen mit
    Record.from_dict(d.copy()) getrennt werden.
    """

    def __init__(self, *args, **kwargs):
        for a in args:
            setattr(self, a, None)
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def __str__(self):
        result = ""
        for attr in self.__dict__:
            val = getattr(self, attr)
            if isinstance(val, str):
                result += f'{attr}: "{val}"\n'
            else:
                result += f'{attr}: {getattr(self, attr)}\n'
        return result

    def __repr__(self):
        first = True
        result = "Record("
        for attr in self.__dict__:
            if getattr(self, attr) is None:
                result += f"'{attr}'" if first else f", '{attr}'"
                first = False
        for attr in self.__dict__:
            if getattr(self, attr) is not None:
                if not first:
                    result += ", "
                val = getattr(self, attr)
                result += f"{attr}=" + f'"{val}"' if isinstance(val, str) else f"{attr}={val}"
                first = False
        result += ')'
        return result

    def as_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, d):
        result = cls()
        result.__dict__ = d
        return result


class TraceVar:
    """
    0.2.0 12.08.2023
    TraceVar implementiert eine überwachte Variable.
    Sie kann bei Schreib- Lese- oder Änderungsoperationen Funktionen aufrufen.

    Erzeugen:
        v = TraceVar(25)
        erzeugt eine Variable mit dem Initialwert 25. Die Angabe des Startwertes ist optional, aber dringend empfohlen.

    Funktionen zuweisen und entfernen:
        Eine Funktion hat immer das Argunent tag. tag gibt optional weitere Informationen zum Auslöser.

        def fn(tag=None):
            print(tag)

        v.trace_add(fn)  # Diese Funktion wird aufgerufen, wenn die Variable geschrieben wird.
        v.trace_add(fn, 'w')  # entspricht v.trace_add(fn).
        v.trace_add(fn, 'c')  # Diese Funktion wird aufgerufen, wenn die Variable geändert wird.
        v.trace_add(fn, 'r')  # Diese Funktion wird aufgerufen, wenn die Variable gelesen wird.
        Optional kann noch ein Tag angegeben werden:
        v.trace_add(fn, 'r', tag='Zusatzinfo')  # Es wird fn('Zusatzinfo') aufgerufen.

        v.trace_remove(fn) # Diese Funktion wird aus der Liste vom Mode 'w' entfernt.
        v.trace_remove(fn, 'w') # Diese Funktion entspricht v.trace_remove(fn).
        v.trace_remove(fn, 'c') # Diese Funktion wird aus der Liste vom Mode 'c' entfernt.
        v.trace_remove(fn, 'r') # Diese Funktion wird aus der Liste vom Mode 'r' entfernt.
        Auch hier muss der korrekte Tag angegeben werden.
        v.trace_remove(fn, 'r', tag='Zusatzinfo') # Bei Funktionen mit Tag muss dieser angegeben werden.

        v.trace_clear() # Löscht alle Funktionen aus allen Listen.
        v.trace('w')  # Löscht alle Funktionen aus der Liste 'w'.
        v.trace_clear('rwc') # Löscht alle Funktionen aus den Listen 'r', 'w' und 'c'.
        # Es sind alle Kombinationen in beliebiger Reihenfolge erlaubt.

    Werte schreiben und lesen:
        v.set(val)
        v.value = val
        val = v.get()
        val = v.value

    Alle Funktionen aufrufen:
        v.trace()       # Alle Fuktionen aus allen Listen aufrufen
        v.trace('w')    # Alle Fuktionen aus der Liste 'w' aufrufen.
        v.trace('rwc')  # Alle Fuktionen aus den listen 'r', 'w' und 'c' aufrufen.
        # Es sind alle Kombinationen in beliebiger Reihenfolge erlaubt.

    """

    def __init__(self, value=None):
        self._value = value
        self.t_write = []
        self.t_read = []
        self.t_change = []

    def trace_add(self, func, mode='w', tag=None):
        if mode == 'w':
            self.t_write.append((func, tag))
        elif mode == 'r':
            self.t_read.append((func, tag))
        elif mode == 'c':
            self.t_change.append((func, tag))

    def trace_remove(self, func, mode='w', tag=None):
        if mode == 'w':
            self.t_write = [item for item in self.t_write if item != (func, tag)]
        elif mode == 'r':
            self.t_read = [item for item in self.t_read if item != (func, tag)]
        elif mode == 'c':
            self.t_change = [item for item in self.t_change if item != (func, tag)]

    def get(self):
        for item in self.t_read:
            item[0](item[1])
        return self._value

    def set(self, value):
        old = self._value
        self._value = value
        for item in self.t_write:
            if item[0] is not None:
                item[0](item[1])
        if old != self._value:
            for item in self.t_change:
                item[0](item[1])

    @property
    def value(self):
        return self.get()

    @value.setter
    def value(self, val):
        self.set(val)

    def trace_clear(self, modes='rwc'):
        if 'r' in modes:
            self.t_read.clear()
        if 'w' in modes:
            self.t_write.clear()
        if 'c' in modes:
            self.t_change.clear()

    def trace(self, modes='rwc'):
        if 'c' in modes:
            for item in self.t_change:
                item[0](item[1])
        if 'w' in modes:
            for item in self.t_write:
                item[0](item[1])
        if 'r' in modes:
            for item in self.t_read:
                item[0](item[1])
        return self

    def all_traces(self):
        traces = Record(w=self.t_write, r=self.t_read, c=self.t_change)
        return traces

class _Globals:
    """
    0.2.0 06.08.2023
    Verwaltung globaler Objekte.
    Ein Wert kann einen beliebigen Typ haben, also auch einfache Werte und Funktionen.
    Es darf nur eine einzige Instanz von Globals() geben. Diese wird nie direkt aufgerufen.

    Ein Objekt wird mit
    - set(name, obj)
    registriert und mit
    - get(name, default)
    wieder abgefragt. Der Default-Wert ist optional.
    Nicht existierende Namen geben None zurück.
    Standardmässig wird ein Fehler generiert, wenn ein bestehender Name nochmals registriert wird.
    Mit overwrite=True kann das Überschreiben eines Wertes erlaubt werden.
    Ist overwrite=False, dann erfolgt kein Überschreiben, die Fehlermeldung kann aber mit
    no_error=True verhindert werden.
    - Globals().get_all()
    gibt das Dictionary mit allen Werten zurück.
    Das zurückgegebene Dictionary kann direkt mutiert werden!
    - remove(name)
    Das Objekt wird aus dem Dictionary entfernt. Das Objekt selbst wird nicht gelöscht.

    Beispiel:
    Globals().set('anzahl', 25)
    anzahl = Globals().get('anzahl')
    """

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
            cls._instance._attributes = {}
        return cls._instance

    def set(self, attribute, obj, overwrite=False, no_error=False):
        if not overwrite:
            if self._attributes.get(attribute) is not None:
                if no_error: return
                raise KeyError('Key is already registered')
        self._attributes[attribute] = obj

    def get(self, attribute, default=None):
        obj = self._attributes.get(attribute)
        if obj is None: obj = default
        return obj

    def remove(self, name):
        self._attributes.pop(name, None)

    def get_all(self):
        return self._instance._attributes.keys()



################### Funktionen ##################
def register_object(name, obj, overwrite=False, no_error=False):
    """
    Standardmässig wird ein Fehler generiert, wenn ein bestehender Name nochmals registriert wird.
    Mit overwrite=True kann das Überschreiben eines Wertes erlaubt werden.
    Ist overwrite=False, dann erfolgt kein Überschreiben, die Fehlermeldung kann aber mit
    no_error=True verhindert werden.
    """
    _Globals().set(name, obj, overwrite, no_error)
    return obj

def get_object(name, default=None):
    obj = _Globals().get(name)
    if obj is None:
        obj = default
        if obj: register_object(name, obj)
    return obj


def unregister_object(name):
    _Globals().remove(name)


