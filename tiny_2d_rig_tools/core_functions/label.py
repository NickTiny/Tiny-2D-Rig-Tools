import textwrap

def split_lines(context, text, parent, split=.5, icon=""):
    chars = int(context.region.width*split)   # 7 pix on 1 character
    wrapper = textwrap.TextWrapper(width=chars)
    text_lines = wrapper.wrap(text=text)
    first = False
    for index, line in enumerate(text_lines):
        if not first and icon != "":
           parent.label(text=line, icon=icon)
           first = True
        else: 
            parent.label(text=line)