import cssutils
import string
from zenlog import log


class TermCss():

    DECORATIONS = {
        'bold': 1,
        'italic': 3,
        'underline': 4,
        'inverse': 7,
    }

    COLORS = {
        'white': 37,
        'grey': 90,
        'gray': 90,
        'black': 30,
        'blue': 34,
        'cyan': 36,
        'green': 32,
        'red': 31,
        'magenta': 35,
        'yellow': 33,
        'none': 0
    }

    BACKGROUNDS = {
        'white': 47,
        'grey': 40,
        'gray': 40,
        'black': 40,
        'blue': 44,
        'cyan': 46,
        'green': 42,
        'red': 41,
        'magenta': 45,
        'yellow': 43,
        'none': 0
    }

    style = None

    def __init__(self, style):
        self.style = style

    @classmethod
    def fromFile(cls, filename):
        return cls(cssutils.parseFile(filename))

    @classmethod
    def fromString(cls, str):
        return cls(cssutils.parseString(str))

    def compile(self, str):

        styled_str = []
        for (text, name, spec, conv) in string.Formatter().parse(str):
            if name:
                (seq, reset) = self.sequence(name)
                styled_str.append(text + seq + "{" + name + "}" + reset)
            else:
                styled_str.append(text)

        styled_str = "".join(styled_str)
        log.d(styled_str)

        return lambda obj: styled_str.format(**obj)

    def sequence(self, name):
        buf = []
        style = self.styles(name)

        # color
        if ('color' in style):
            try:
                buf.append(self.COLORS[style['color']])
            except KeyError:
                log.w("{} is an invalid color name".format(style['color']))

        # background
        if ('background' in style):
            try:
                buf.append(self.BACKGROUNDS[style['background']])
            except KeyError:
                log.w("{} is an invalid background color name".format(style['background']))

        # text-decoration
        if ('text-decoration' in style):
            try:
                buf.append(self.DECORATIONS[style['text-decoration']])
            except KeyError:
                log.w("{} is an unsuppoted text-decoration".format(style['textdecoration']))

        # text-decoration
        if ('font-weight' in style):
            try:
                buf.append(self.DECORATIONS[style['font-weight']])
            except KeyError:
                log.w("{} is an unsuppoted font-weight".format(style['font-weight']))

        # text-style
        if ('font-style' in style):
            try:
                buf.append(self.DECORATIONS[style['font-style']])
            except KeyError:
                log.w("{} is an unsuppoted font-style".format(style['font-style']))

        _seq = ";".join([str(n) for n in buf])
        seq = "" if _seq is None else "\033[{}m".format(_seq)
        reset = "" if _seq is None else "\033[0m"

        return (seq, reset)

    def styles(self, name):
        styles = {}

        for rule in self.style:
            if (name != rule.selectorText):
                continue
            for p in rule.style:
                styles[p.name] = p.value

        return styles
