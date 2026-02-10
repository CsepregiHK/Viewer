"""
 Copyright (c) 2025 free

 Permission is hereby granted, free of charge, to any person obtaining a copy of
 this software and associated documentation files (the "Software"), to deal in
 the Software without restriction, including without limitation the rights to
 use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 the Software, and to permit persons to whom the Software is furnished to do so,
 subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 """

import streamlit as st

def wuifunc(_searchobject):

    st.title("A rövid húszadik század")
    doe = st.text_input(label='Dátum:', placeholder='ÉÉÉÉ.HH.NN', 
                            label_visibility = 'hidden', width=120)
    doe_string = doe
        
    if doe_string != "":
        for result in _searchobject.run_search(doe_string):
            date = result[0]
            title = result[1]
            text = result[2]
            spos = result[3]
            epos = result[4]
            if(spos > 0):
                text_1 = text[:spos]
                text_2 = text[spos:epos]
                text_3 = text[epos:]
                st.subheader(date)
                st.subheader(title)
                st.html(text_1 + "<span style='text-decoration: none; box-shadow: inset 0 -.5em 0 rgba(255,166,60,0.75); color: inherit;'>" + text_2 + "</span>" + text_3)
            else:
                st.write("Nincs bejegyzés a kért dátumra, a következő dátumhoz tartozó bejegyzést mutatjuk.")
                st.subheader(date)
                st.subheader(title)
                st.html(text)
    else:
        st.write("Kérem, adjon meg egy dátumot!")

@st.cache_resource
def init(_searchobject):
    _searchobject.load_data()