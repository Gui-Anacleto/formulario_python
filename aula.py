from tkinter import *
from tkinter import ttk
import sqlite3

root = Tk()

    
class Funcs():
    def limpa_tela(self):
        self.cod.delete(0, END)
        self.nome.delete(0, END)
        self.telefone.delete(0, END)
        self.cidade.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.bd")
        self.cursor = self.conn.cursor();print("Conectando ao banco de dados")
    def desconecta_bd(self):
        self.conn.close();print("Desconectando do banco de dados")
    def montaTabelas(self):
        self.conecta_bd()
        #Cria tabela caso ela nao exista
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade CHAR(40)
            );
        """)
        self.conn.commit();print("Banco de dados criado")
        self.desconecta_bd()
    def variaveis(self):
        self.codigo_add = self.cod.get()
        self.nome_add = self.nome.get()
        self.telefone_add = self.telefone.get()
        self.cidade_add = self.cidade.get()
    def OnDoubleClick(self,event):
        self.limpa_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, "values")
            self.cod.insert(END, col1)
            self.nome.insert(END, col2)
            self.telefone.insert(END, col3)
            self.cidade.insert(END, col4)         
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """,(self.codigo_add))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()
    def alterar_cliete(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade= ?
        WHERE cod = ?""",(self.nome_add,self.telefone_add,self.cidade_add,self.codigo_add))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def add_Cliente(self): 
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""
        INSERT INTO clientes (nome_cliente, telefone, cidade)
        VALUES (?,?,?)""",(self.nome_add, self.telefone_add, self.cidade_add) 
        )
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()

        lista = self.cursor.execute("""
        SELECT cod, nome_cliente, telefone, cidade FROM clientes 
        ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()

    def busca_Cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())
        self.nome.insert(END, '%')
        nome = self.nome.get()
        self.cursor.execute(""" 
        SELECT cod, nome_cliente, telefone, cidade FROM clientes
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % nome)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("", END, values=i)
        self.limpa_tela()
        self.desconecta_bd()
class Application(Funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frame_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.limpa_tela()
        self.montaTabelas()
        self.select_lista()
        self.menus()
        root.mainloop()
    def tela(self):
        self.root.title("Principal")
        self.root.resizable(False, False)
        self.root.geometry("700x500")
        self.root.resizable(True,True)
        self.root.configure(background = "#708090");
        self.root.maxsize(width= 900, height=700)
        self.root.minsize(width= 500, height=400)
    def frame_da_tela(self):
        self.frame1 = Frame(self.root, bd=4, highlightbackground="#6495ED", highlightthickness=2)
        self.frame1.place(relx=0.02 , rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame2 = Frame(self.root, bd=4, highlightbackground="#6495ED", highlightthickness=2)
        self.frame2.place(relx=0.02 , rely=0.5, relwidth=0.96, relheight=0.46)
    def widgets_frame1(self):
        self.bt_limpar = Button(self.frame1, text="Limpar", bd=2, bg="#DCDCDC" , fg = "Black" , font =("Arial", 11), command= self.limpa_tela)
        self.bt_limpar.place(relx = 0.2, rely=0.1, relwidth=0.1 , relheight=0.15)
        
        self.bt_buscar = Button(self.frame1, text="Buscar", bd=2, bg="#DCDCDC" , fg = "Black" , font =("Arial", 11), command= self.busca_Cliente)
        self.bt_buscar.place(relx = 0.3, rely=0.1, relwidth=0.1 , relheight=0.15)

        self.bt_novo = Button(self.frame1, text="Novo", bd=2, bg="#DCDCDC" , fg = "Black" , font =("Arial", 11) , command=self.add_Cliente)
        self.bt_novo.place(relx = 0.5, rely=0.1, relwidth=0.1 , relheight=0.15)
       
        self.bt_alterar = Button(self.frame1, text="Alterar", bd=2, bg="#DCDCDC" , fg = "Black" , font =("Arial", 11), command= self.alterar_cliete)
        self.bt_alterar.place(relx = 0.6, rely=0.1, relwidth=0.1 , relheight=0.15)

        self.bt_apagar = Button(self.frame1, text="Apagar", bd=2, bg="#DCDCDC" , fg = "Black" , font =("Arial", 11), command=self.deleta_cliente)
        self.bt_apagar.place(relx = 0.7, rely=0.1, relwidth=0.1 , relheight=0.15)

        self.lb_cod = Label(self.frame1, text="Código", fg = "Black" , font =("Arial", 11))
        self.lb_cod.place(relx = 0.05, rely=0.05)

        self.cod = Entry(self.frame1, bg="lightgray", font=("Arial", 10, "bold"))
        self.cod.place(relx = 0.04, rely=0.15,relwidth=0.11)

        self.lb_nome = Label(self.frame1, text="Nome", fg = "Black" , font =("Arial", 11))
        self.lb_nome.place(relx = 0.05, rely=0.35)

        self.nome = Entry(self.frame1)
        self.nome.place(relx = 0.04, rely=0.45,relwidth=0.86)

        self.lb_Telefone = Label(self.frame1, text="Telefone",fg = "Black" , font =("Arial", 11))
        self.lb_Telefone.place(relx = 0.05, rely=0.6)

        self.telefone = Entry(self.frame1)
        self.telefone.place(relx = 0.04, rely=0.7,relwidth=0.4)

        self.lb_Cidade = Label(self.frame1, text="Cidade",fg = "Black" , font =("Arial", 11))
        self.lb_Cidade.place(relx = 0.5, rely=0.6)

        self.cidade = Entry(self.frame1)
        self.cidade.place(relx = 0.5, rely=0.7,relwidth=0.4)
    def lista_frame2(self):

        self.listaCli = ttk.Treeview(self.frame2, height=3, column=("col1", "col2", "col3", "col4"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Código")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="Telefone")
        self.listaCli.heading("#4", text="Cidade")

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=125)

        self.listaCli.place(relx = 0.01, rely=0.1, relwidth=0.95 , relheight=0.85)

        self.scrooLista = Scrollbar(self.frame2, orient="vertical")
        self.listaCli.configure(yscroll=self.scrooLista.set)
        self.scrooLista.place(relx=0.96, rely=0.1 , relwidth=0.04, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)
    def menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()
        menubar.add_cascade(label="Opções", menu= filemenu)
        menubar.add_cascade(label="Sobre", menu= filemenu2)

        filemenu.add_cascade(label="Sair", command=Quit)
        filemenu2.add_cascade(label="Limpa Cliente", command=self.limpa_tela)

Application()