"""Diagrama paso a paso del ejercicio 28. Requiere Python con tkinter."""
import tkinter as tk
from tkinter import ttk


def fmt(v):
    return f'{v:.6g}'


class App:
    def __init__(self, root):
        self.root = root
        root.title('Ejercicio 28 · Retardos y sumadores')
        root.geometry('1320x900')
        root.minsize(1000, 760)
        top = ttk.Frame(root, padding=10); top.pack(fill='x')
        ttk.Label(top, text='Condiciones iniciales:').pack(side='left')
        self.ic = tk.StringVar(value='Nulas')
        ttk.Combobox(top, textvariable=self.ic, values=['Nulas', 'Inciso b'], state='readonly', width=12).pack(side='left', padx=6)
        ttk.Button(top, text='Reiniciar con estas condiciones', command=self.reset).pack(side='left', padx=8)
        self.auto = tk.BooleanVar(value=False)
        ttk.Checkbutton(top, text='Entrada automática: x[n] = (0.5)ⁿ u[n]', variable=self.auto, command=self.mode).pack(side='left', padx=12)
        bar = ttk.Frame(root, padding=10); bar.pack(fill='x')
        self.clock = ttk.Label(bar, font=('Arial', 13, 'bold'));self.clock.pack(side='left', padx=8)
        ttk.Label(bar, text='x[n] =').pack(side='left')
        self.input = tk.StringVar(value='1')
        self.entry = ttk.Entry(bar, textvariable=self.input, width=14);self.entry.pack(side='left', padx=5)
        self.calc = ttk.Button(bar, text='Ingresar y avanzar →', command=self.calculate);self.calc.pack(side='left', padx=8)
        self.back = ttk.Button(bar, text='← Volver atrás', command=self.undo);self.back.pack(side='left', padx=8)
        self.entry.bind('<Return>', self.calculate)
        self.message = ttk.Label(root, padding=(15, 4));self.message.pack(fill='x')
        self.canvas = tk.Canvas(root, bg='#fafafa', height=440, highlightthickness=0);self.canvas.pack(fill='both', expand=True)
        self.canvas.bind('<Configure>', lambda e:self.draw())
        self.sumtext = ttk.Label(root, padding=10, font=('Arial', 12));self.sumtext.pack(fill='x')
        self.table = ttk.Treeview(root, columns=('n','x','x1','x2','y1','y2','y'), show='headings', height=7)
        for key, label in zip(self.table['columns'], ['n','x[n]','x[n−1]','x[n−2]','y[n−1]','y[n−2]','y[n]']):
            self.table.heading(key, text=label);self.table.column(key, width=120, anchor='center')
        self.table.pack(fill='x', padx=12, pady=8)
        ttk.Label(root, text='z⁻¹ guarda un valor durante un período de muestreo. Valores de señal sin ponderar. Σ muestra la suma con coeficientes aplicados.', padding=(12,5)).pack(fill='x')
        self.reset()

    def reset(self):
        self.n=0;self.x1=0.;self.x2=0.
        self.y1,self.y2=(11/6,37/36) if self.ic.get()=='Inciso b' else (0.,0.)
        self.x=None;self.y=None;self.history=[]
        self.input.set('1')
        self.table.delete(*self.table.get_children())
        self.sumtext.config(text='y[n] = 3x[n−1] + 5x[n−2] + 5y[n−1] − 6y[n−2]')
        self.refresh()

    def mode(self):
        if self.auto.get():self.input.set(fmt(.5**self.n))
        self.entry.config(state='disabled' if self.auto.get() else 'normal')

    def refresh(self):
        self.clock.config(text=f'Próximo instante: n = {self.n}')
        self.back.config(state='normal' if self.history else 'disabled')
        self.message.config(text='Ingresá x[n] y presioná Enter o «Ingresar y avanzar». El diagrama muestra las memorias del próximo instante.')
        self.mode();self.draw()

    def calculate(self, event=None):
        import math
        try:
            x=.5**self.n if self.auto.get() else float(self.input.get().replace(',','.'))
            if not math.isfinite(x):raise ValueError
        except ValueError:
            self.message.config(text='Ingresá un número real finito para x[n].');return
        parts=[3*self.x1,5*self.x2,5*self.y1,-6*self.y2]
        y=sum(parts)
        if not math.isfinite(y):
            self.message.config(text='La salida supera el rango numérico. Reiniciá o volvé atrás.');return
        self.history.append((self.n,self.x1,self.x2,self.y1,self.y2,x))
        row=self.table.insert('', 'end', values=[self.n]+[fmt(v) for v in [x,self.x1,self.x2,self.y1,self.y2,y]])
        self.table.see(row)
        self.sumtext.config(text=f'Último cálculo: y[{self.n}] = '+' + '.join(f'({fmt(p)})' for p in parts)+f' = {fmt(y)}')
        self.x2,self.x1=self.x1,x
        self.y2,self.y1=self.y1,y
        self.n+=1
        if not self.auto.get():self.input.set('1')
        self.refresh()
        if not self.auto.get():self.entry.focus_set()

    def undo(self):
        if not self.history:return
        self.n,self.x1,self.x2,self.y1,self.y2,x=self.history.pop()
        rows=self.table.get_children()
        if rows:self.table.delete(rows[-1])
        self.input.set(fmt(x))
        self.sumtext.config(text=f'Volviste a n = {self.n}. Podés modificar la entrada y repetir este paso.')
        self.refresh()

    def draw(self):
        c=self.canvas;c.delete('all')
        # Una sola escala para ambos ejes: todos los sumadores son círculos.
        w=max(c.winfo_width(),1);h=max(c.winfo_height(),1)
        scale=min(w/1200,h/500)
        ox=(w-1200*scale)/2;oy=(h-500*scale)/2
        def coords(points):
            return [v*scale+(ox if i%2==0 else oy) for i,v in enumerate(points)]
        def text(x,y,label,color='#334155'):
            c.create_text(*coords([x,y]),text=label,fill=color,font=('Arial',max(8,round(12*scale))))
        def line(points,color='#334155',arrow=True):
            c.create_line(*coords(points),fill=color,width=2,arrow='last' if arrow else 'none')
        def dot(x,y,color):
            c.create_oval(*coords([x-3,y-3,x+3,y+3]),fill=color,outline=color)
        def summer(x,y,value):
            c.create_oval(*coords([x-19,y-19,x+19,y+19]),fill='white',outline='black',width=2)
            text(x,y,'+','black')
            text(x+65,y+25,f'Σ = {fmt(value)}','black')
        def delay(x,y):
            c.create_rectangle(*coords([x-29,y-25,x+29,y+25]),fill='white',outline='#334155',width=2)
            text(x,y,'z⁻¹')
        blue='#1769aa';orange='#b45309'
        text(600,24,f'Memorias disponibles para calcular y[{self.n}]')
        direct=3*self.x1+5*self.x2
        feedback=5*self.y1-6*self.y2
        total=direct+feedback
        current=fmt(.5**self.n) if self.auto.get() else '?'
        # b_k son ganancias directas; -a_k son las de realimentación.
        # La normalización de salida es 1/a_0 (no 1/a_k).
        line([65,100,361,100],blue)
        text(92,70,'x[n]',blue);text(92,127,current,blue)
        dot(200,100,blue)
        text(285,63,'b₀ = 0',blue)
        summer(380,100,direct)
        line([399,100,741,100])
        
        
        summer(760,100,total)
        line([779,100,1140,100],orange)
        text(900,78,'1/a₀ = 1',orange)
        text(920,127,f'y[n] = {fmt(total)}',orange)
        # Entrada: retardos en orden descendente.
        line([200,100,200,165],blue);delay(200,190)
        
        line([200,215,200,280],blue);dot(200,280,blue)
        line([200,280,361,280],blue);summer(380,280,direct)
        text(280,240,'b₁ = 3',blue)
        
        line([380,261,380,119])
        
        
        line([200,280,200,345],blue);delay(200,370)
        
        line([200,395,200,450,380,450,380,299],blue)
        text(445,375,'b₂ = 5',blue)
        
        text(100,263,'x[n−1]',blue);text(100,292,fmt(self.x1),blue)
        text(100,428,'x[n−2]',blue);text(100,458,fmt(self.x2),blue)
        # Salida y memorias de realimentación.
        dot(1000,100,orange);line([1000,100,1000,165],orange);delay(1000,190)
        
        line([1000,215,1000,280],orange);dot(1000,280,orange)
        line([1000,280,779,280],orange);summer(760,280,feedback)
        text(885,240,'−a₁ = 5',orange)
        
        line([760,261,760,119])
        
        
        line([1000,280,1000,345],orange);delay(1000,370)
        
        line([1000,395,1000,450,760,450,760,299],orange)
        text(670,375,'−a₂ = −6',orange)
        
        text(1100,263,'y[n−1]',orange);text(1100,292,fmt(self.y1),orange)
        text(1100,428,'y[n−2]',orange);text(1100,458,fmt(self.y2),orange)
        # Dibujar las pelotitas al final para que tapen la línea bajo ellas.
        def ball(x,y,value,color):
            label=str(value)
            radius=25
            c.create_oval(*coords([x-radius,y-radius,x+radius,y+radius]),
                          fill='#fde047',outline='#ca8a04',width=1.5)
            size=max(6,round(min(12,75/max(1,len(label)))*scale))
            c.create_text(*coords([x,y]),text=label,fill=color,font=('Arial',size,'bold'))
        # Centro del último segmento recto antes de cada sumador.
        ball((200+361)/2,100,current,blue)
        ball((200+361)/2,280,fmt(self.x1),blue)
        ball(380,(450+299)/2,fmt(self.x2),blue)
        ball(380,(261+119)/2,fmt(direct),'black')
        ball((399+741)/2,100,fmt(direct),'black')
        ball((1000+779)/2,280,fmt(self.y1),orange)
        ball(760,(450+299)/2,fmt(self.y2),orange)
        ball(760,(261+119)/2,fmt(feedback),'black')
        text(570,483,'Señal sin ponderar · Σ: resultado con coeficientes aplicados','black')


if __name__=='__main__':
    root=tk.Tk();App(root);root.mainloop()
