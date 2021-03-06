def pgf2eps(PGFfig, preamble=[]):
    import subprocess as sp
    import os
    PGFfile = PGFfig + '.pgf'
    with open(PGFfig + '.tex', 'w') as tmp:
        tmp.write(r"\documentclass[crop]{standalone}")
        for line in preamble:
            tmp.write(line)
            tmp.write("\n")

        tmp.write(r"""
\usepackage{pgf}

\begin{document}
\input{%s.pgf}
\end{document}
""" % PGFfig
        )

        tmp.close()

        sp.call(['latex', PGFfig])
        sp.call(['dvips', '-z', PGFfig + '.dvi', '-o'])
        print "\n\n**** Generating EPS\n"
        sp.call(['ps2eps',
                 '-f',
                 '-O',
                 '-a',
                 '-d',
                 '-W',
                 '--resolution=300',
                 PGFfig + '.ps'
        ])
        sp.call(['rm', '-f',
                 PGFfig + '.tex',
                 PGFfig + '.dvi',
                 PGFfig + '.ps',
                 PGFfig + '.aux',
                 PGFfig + '.log',
        ])
