

DEF_HIDE_UNDERS = True
DEF_INDENT_WIDTH = 2
DEF_MAX_INDENT = 20

def _dump_print(text: str, indent: int, indent_width: int = DEF_INDENT_WIDTH):
    print("{o}{text}".format(o=' ' * indent * indent_width, text=text))
    if indent > 20:
        exit(666)

def _dump(thing: any, name: str = '', indent: int = 0, hide_unders: bool = DEF_HIDE_UNDERS, indent_width: int = DEF_INDENT_WIDTH, max_indent: int = DEF_MAX_INDENT):

    def name_prefix(name:str) -> str:
        return "'{}': ".format(name) if name else ""

    def named_thing(name:str, thing: str) -> str:
        return '{}{}'.format(name_prefix(name), thing)

    if len(name) > 0 and name[0] == '_' and hide_unders:
        return

    if len(name)== 0 and thing is None:
        return

    if indent > max_indent:
        print("Dumpster: max indent ({max}) reached".format(max=max_indent))

    if name and thing is None:
        _dump_print(name, indent, indent_width)
        return

    if isinstance(thing, str):
        _dump_print(named_thing(name, thing), indent, indent_width)
        return
    
    if isinstance(thing, list) or isinstance(thing, set):
        if len(thing) == 0:
            _dump(thing=named_thing(name, '[]'), indent=indent, hide_unders=hide_unders, indent_width=indent_width, max_indent=max_indent)
        else:
            _dump(thing=named_thing(name, '['), indent=indent, hide_unders=hide_unders, indent_width=indent_width, max_indent=max_indent)
            for item in thing:
                _dump(thing=item if item else 'None', indent=indent+1, hide_unders=hide_unders, indent_width=indent_width, max_indent=max_indent)
            _dump(thing=']', indent=indent, hide_unders=hide_unders, indent_width=indent_width, max_indent=max_indent)
        return

    if isinstance(thing, dict):
        _dump(thing=named_thing(name, '{'), indent=indent, hide_unders=hide_unders, indent_width=indent_width, max_indent=max_indent)

        for key in thing.keys():
            _dump(thing=thing[key] if thing[key] else 'None', name=key, indent=indent+1, hide_unders=hide_unders, indent_width=indent_width, max_indent=max_indent)

        _dump(thing='}', indent=indent, hide_unders=hide_unders, indent_width=indent_width, max_indent=max_indent)
        return

    if hasattr(thing, '__dict__'):
        _dump(thing=vars(thing), name=name, indent=indent, hide_unders=hide_unders, indent_width=indent_width, max_indent=max_indent)
        return

    _dump_print(named_thing(name, thing), indent, indent_width)

def dump(thing: any, name: str = '', hide_unders: bool = DEF_HIDE_UNDERS, indent_width: int = DEF_INDENT_WIDTH, max_indent: int = DEF_MAX_INDENT):
    _dump(thing, name, 0, hide_unders, indent_width, max_indent)

