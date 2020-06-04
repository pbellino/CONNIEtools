import subprocess
import os

preamble = r'''
\documentclass{beamer}
%
% Choose how your presentation looks.
%
% For more themes, color themes and font themes, see:
% http://deic.uab.es/~iblanes/beamer_gallery/index_by_theme.html
%
\mode<presentation>
{
  \usetheme{default}      % or try Darmstadt, Madrid, Warsaw, ...
  \usecolortheme{default} % or try albatross, beaver, crane, ...
  \usefonttheme{default}  % or try serif, structurebold, ...
  \setbeamertemplate{navigation symbols}{}
  \setbeamertemplate{caption}[numbered]
  \setbeamertemplate{footline}[frame number]
} 

\usepackage[english]{babel}
\usepackage[utf8x]{inputenc}
\usepackage{hyperref}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{nath}
\delimgrowth=1
\setlength{\mathindent}{-1in}

\usefonttheme{professionalfonts}

\lstset{
language=Python,
breakatwhitespace=true,
breaklines=true,
basicstyle=\sffamily\tiny,
keywordstyle=\bf\color{blue},
showtabs=true,
tabsize=2,
% digitstyle=\color{red},
% otherstyle=\color{red},
numberstyle=\color{red},
columns=fullflexible,
% commentstyle=\sf\tiny\color{gray},
% stringstyle=\color{red},
showstringspaces=false,
morekeywords={as},
% emph={(,)},
% emphstyle=\color{blue},
numbers=left
% identifierstyle=\color{blue}
}
\lstset{literate={-}{-}1}
\title[Size Like]{simulation tools}
\author{Philipe Mota}
\institute{CBPF}
\date{\today}

\begin{document}

\begin{frame}
  \titlepage
\end{frame}
'''

B = '\n'

class Beamer:
    def writelines( self, s, mode = 'a' ):
        open( '%s.tex' % (self.fname+'/'+self.fname), mode ).writelines( s )
    
    def __init__(self, fname='calculations'):
        self.fname = fname
        self.writelines( preamble, mode = 'w' )
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.writelines( [r'\end{document}'] )
        self.pdflatex()
    
    def par( self, s ):
        self.writelines( [s + '\n'] )

    equation_evironment = 'equation'
    def pdflatex( self ):
        subprocess.check_output(['pdflatex', '%s.tex' % (self.fname+'/'+self.fname)])

    def section( self, text ):
        self.writelines( [ r'\section{%s}' % text] )
    
    def environment( self, s, env = 'equation' ):
        self.writelines( [r'\begin{%s}' % env] )
        self.writelines( s )
        self.writelines( [r'\end{%s}' % env] )

    def eq( self, lhs, rhs = None, mathmode = 'equation' ):
        #print 'eq', lhs
        r = [r'\begin{%s}'%mathmode, lhs]
        if not rhs is None:
            if type(rhs) is list or type(rhs) is tuple:
                r += ['=', r'\\ '.join(rhs)]
            else:
                r += ['=', rhs]
        r += [r'\end{%s}'%mathmode]
        self.writelines( r )

    def math( self, lhs, rhs = None, label = None ):
        #print 'eq', label
        r = [r'\begin{equation}', latex(lhs)]
        if not rhs is None:
            r += ['=', latex(rhs)]
        if not label is None:
            r += [r'\label{%s}'%label]
        r += [r'\end{equation}']
        self.writelines( r )

    def matheval( self, s ):
        #print 'eq', label
        self.writelines( [r'\begin{equation}', latex(eval(m)), r'\label{%s}'%m, r'\end{equation}'] )

    def frame( self, title, *args ):
        s = r'\begin{frame}[fragile]{%s}' % title + B*3
        for arg in args:
            s += arg #+ B*2
        s += B + r'\end{frame}' + B*3
        self.writelines( s )

    def code( self, c=None, language=None, file=None, func=None ):
        if file:
            if not os.path.exists('%s/%s' % (self.fname,file)):
                print( 'running function' )
                func()
            return r'\lstinputlisting{{{}}}'.format(self.fname+'/'+file)+B
        s = r'\begin{lstlisting}[language=%s]' % (language) + B
        s += c
        s += r'\end{lstlisting}' + B
        return s
    
    def column( self, *args ):
        s = ''
        s += r'\begin{columns}'+B
        for arg in args:
            s += r'\column{%s\paperwidth}'%(1./len(args))+B
            s += arg+B
        s += r'\end{columns}'+B
        return s
    
    def center(self, *lines ):
        s = r'\begin{center}' + B
        for line in lines:
            s += line
        s += r'\end{center}' + B
        return s
        
    
    def figure( self, path, width=None, height=None, scale=None, s='', frame=False, func=None ):
        #if frame: s += r'\frame{' + B
        fname = self.fname+'/'+path
        if not os.path.exists(fname):
            print( 'running function' )
            func()
            #print( '%s does not exist' % fname )
            #s += r'{{\it figure {fname} }}'.format(fname=fname) + B
        
        if width is not None:
            s += r'\includegraphics[width={width}\columnwidth]{{{fname}}}'.format(width=width, fname=fname) + B 
        elif height is not None:
            s += r'\includegraphics[height={height}\paperheight]{{{fname}}}'.format(height=height, fname=fname) + B
        elif scale is not None:
            s += r'\includegraphics[scale={scale}]{{{fname}}}'.format(scale=scale, fname=fname) + B
        else:
            raise Exception('missing heigh or width')
        #if frame: s += '}' + B
        return s
        
    def table( self, file, fontsize=12, spacing=15, func=None ):
        s = ''
        if not os.path.exists('%s/%s' % (self.fname,file)):
            print( 'running function' )
            func()
        s += r'{{\fontsize{{{}}}{{{}}}\selectfont'.format(fontsize,spacing)+B
        s += r'{\setlength{\tabcolsep}{0.5em}'+B
        for line in open('%s/%s' % (self.fname,file), 'r'):
            args = line.strip('\n').split(',')
            if '#' in line:
                args[0] = args[0].strip('#')
                s += r'\begin{{tabular}}{{ {} }}'.format('r'*len(args)) +B
            s += ' & '.join( args ) + r'\\' + B
        s += r'\end{tabular}'+B
        s += r'}'+B
        s += r'}'+B
        return s
    
def openBeamer( fname ): return Beamer( fname )