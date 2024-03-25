from datetime import datetime
from fpdf import FPDF
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

#ticket = ["2 - filete de ternera - 30.23","4 - coca cola - 4.20","-2 - coca cola - 1.40", "1 - pan - 0.90"]

producSuper = ["filete de ternera - 30.23","coca cola - 4.20","pan - 0.90", "muslos de pollo - 3.50"]

compra = []

def comprobarTicket(ticket):
    listTicket=[]
    dicTicket={}
    if isinstance(ticket,list):
        for forTicket in ticket:
            cantidad = 0
            producto = ""
            precio = 0
            splitTicket = forTicket.split(" - ")
            #comprobamos si el array consta de tres datos. no ponemos float por que no podemos comprar medio producto.
            if len(splitTicket)!=3:
                messagebox.showinfo("Error","Hay un error en la lista de la compra (numero de campos incorrectos)")
                
            #comprobamos que el primero dato es un int
            try:
                cantidad = int(splitTicket[0])
            except ValueError:
                messagebox.showinfo("Error","Hay un error en la lista de la compra (alguna cantidad)")
                

            #Nos aseguramos de que el segundo dato es un string.
            if isinstance(splitTicket[1],str):
                producto = splitTicket[1]
                if producto.strip() == "":
                    messagebox.showinfo("Error","Hay un error en la lista de la compra (Falta un producto)")
                    
            else:
                messagebox.showinfo("Error","Hay un error en la lista de la compra (algún producto)")

            #comprobamos que el tercer dato es un float
            try:
                precio = float(splitTicket[2])
            except ValueError:
                messagebox.showinfo("Error","Hay un error en la lista de la compra (algún precio)")

            #creamos un diccionario
            dicTicket = {"cantidad":cantidad, "producto":producto, "precio":precio}
            listTicket.append(dicTicket)

        #creamos una lista con los diccionarios de productos.
        return listTicket
        
    else:
        messagebox.showinfo("Error","Hay un error en la lista de la compra (no ha pasado una lista)")

def comProducSuper(producSuper):
    listProduc=[]
    dicProduc={}
    if isinstance(producSuper,list):
        for forProduc in producSuper:
            producto = ""
            precio = 0
            splitProduc = forProduc.split(" - ")
            #comprobamos si el array consta de tres datos. no ponemos float por que no podemos comprar medio producto.
            if len(splitProduc)!=2:
                messagebox.showinfo("Error","Hay un error en la lista de la compra (numero de campos incorrectos)")
                
                
            #Nos aseguramos de que el segundo dato es un string.
            if isinstance(splitProduc[0],str):
                producto = splitProduc[0]
                if producto.strip() == "":
                    messagebox.showinfo("Error","Hay un error en los productos del supermercado (Falta un producto)")
                    
            else:
                messagebox.showinfo("Error","Hay un error en los productos del supermercado (algún producto)")
            #comprobamos que el tercer dato es un float
            try:
                precio = float(splitProduc[1])
            except ValueError:
                messagebox.showinfo("Error","Hay un error en los productos del supermercado (algún precio)")
            #creamos un diccionario
            dicProduc = {"producto":producto, "precio":precio}
            listProduc.append(dicProduc)

        #creamos una lista con los diccionarios de productos.
        return listProduc
        
    else:
        messagebox.showinfo("Error","Hay un error en la lista de la compra (no ha pasado una lista)")


def productosSuper(producSuper):
    productos = comProducSuper(producSuper)
    listaProductos = []
    for producTicket in productos:
        if producTicket["producto"] != "":
            listaProductos.append(producTicket["producto"])
    return listaProductos

"""def productosTicket(ticket):
    productos = comprobarTicket(ticket)
    listaProductos = []
    for producTicket in productos:
        if producTicket["cantidad"]>0:
            listaProductos.append(producTicket["producto"])
    return listaProductos"""

def obtenerPrecio(producto):
    for listaProductos in comProducSuper(producSuper):
        if producto == listaProductos["producto"]:
            precioProducto = listaProductos["precio"]
            return precioProducto
    return ""

def actualizarPrecio(event):
    productoSeleccionado = boxProductos.get()
    precio = obtenerPrecio(productoSeleccionado)
    precioProducto.set(precio)

def comprarProducto():
    productoExite=False
    cantidad = textoCantidad.get().strip()
    producto = boxProductos.get().strip()
    precio = textoPrecio.get()
    listaCompra = comprobarTicket(compra) 
    if producto == "":
        messagebox.showerror("Error","No se ha seleccionado producto")
        return
    try:
        cantidad = int(cantidad)
        if cantidad>0:
            for productos in listaCompra:
                if productos["producto"] == producto:
                    productos["cantidad"] = productos["cantidad"]+cantidad
                    actualizarCompra(listaCompra)
                    imprimirCompra(compra)
                    productoExite = True
                    return
        elif cantidad==0:
            messagebox.showerror("Error","La cantidad es 0")
            return
        else:
            messagebox.showerror("Error","La cantidad es erronea")
            return
        if not productoExite:
            nuevoProducto = f"{cantidad} - {producto} - {precio}"
            compra.append(nuevoProducto)

        textoCantidad.delete(0, END)
        precioProducto.set("")
        boxProductos.set("")

        imprimirCompra(compra)

    except ValueError:
        messagebox.showerror("Error","La cantidad comprada es erronea")

        textoCantidad.delete(0, END)
        precioProducto.set("")
        boxProductos.set("")

def descontarProducto():
    cantidad = textoCantidad.get()
    producto = boxProductos.get()
    listaCompra = comprobarTicket(compra)
    if producto != "":
        try:
            cantidad = int(cantidad)
            if cantidad>0:
                for prodCompra in listaCompra:
                    if prodCompra["producto"] == producto:
                        totalProducto = prodCompra["cantidad"] - cantidad
                        if totalProducto > 0:
                            prodCompra["cantidad"] = totalProducto
                            textoCantidad.delete(0, END)
                            precioProducto.set("")
                            boxProductos.set("")
                        elif totalProducto==0:
                            listaCompra.remove(prodCompra)
                            textoCantidad.delete(0, END)
                            precioProducto.set("")
                            boxProductos.set("")
                        else:
                            messagebox.showerror("Error",f"No has comprados tantos {producto}")
                            textoCantidad.delete(0, END)
                            precioProducto.set("")
                            boxProductos.set("")
            elif cantidad==0:
                messagebox.showerror("Error","La cantidad es 0")
                return
            else:
                messagebox.showerror("Error","La cantidad es negativa")
                return
        except ValueError:
            messagebox.showerror("Error","La cantidad comprada es erronea")

            textoCantidad.delete(0, END)
            precioProducto.set("")
            boxProductos.set("")
    else:
        messagebox.showerror("Error","No has elegido ningún producto")
    actualizarCompra(listaCompra)
    imprimirCompra(compra)

def imprimirCompra(compra):
    textoCompra.delete('1.0',END)
    productos = comprobarTicket(compra)
    totalCompra = precioTotal(compra)
    
    for producto in productos:
        
        listaCompra = f"nº:{producto["cantidad"]}  producto:{producto["producto"]}  €:{producto["precio"]}"
        textoCompra.insert(END,listaCompra + "\n")

    textoCompra.insert(END,f"Total compra: {totalCompra} \n")

def precioTotal(compra):
    listTicket = comprobarTicket(compra)
    total = 0
    iva = 16
    
    for fotListTicket in listTicket:
        if fotListTicket["cantidad"]<0:
            
            total = total - (abs(fotListTicket["cantidad"])*fotListTicket["precio"])
        else:
            total = total + (fotListTicket["cantidad"]*fotListTicket["precio"])
        
    
    if total < 0:
        return "Error en la lista de la compra (la cantidad es negativa)"
    else:
        #incrementarle un 16%
        total = total + (total * (iva/100))
        
        return round(total,2)


def ingresarProducto():
        global producSuper
        productoExiste = False
        productosSupermercado = comProducSuper(producSuper)
        productoNew = textoProducNew.get().strip()
        precioNew = textoPrecioNew.get().strip()
        
        for productos in productosSupermercado:
            if productos["producto"] == productoNew:
                productoExiste=True
            else:
                productoExiste=False

        if productoExiste == False:
            if productoNew != "":
                if precioNew != "":
                    try:
                        precioNew=float(precioNew)
                        producSuper.append(f"{productoNew} - {precioNew}")
                        messagebox.showinfo("Trabajo realizado","Producto ingresado con exito")
                        actualizarProductos()
                        textoProducNew.delete(0, END)
                        textoPrecioNew.delete(0, END)
                    except ValueError:
                        messagebox.showerror("Error","Hay un error en el precio")
                else:
                    messagebox.showerror("Error","No has ingresado el precio")
            else:
                messagebox.showerror("Error","No has ingresado ningún producto")
        else:
            messagebox.showerror("Error","El producto ya existe")

def delProducSuper():
    delProducto = boxDelProduc.get().strip()
    proListaSuper = comProducSuper(producSuper)
    proListaSuper = [producto for producto in proListaSuper if producto["producto"] != delProducto ]
  
    messagebox.showinfo("Trabajo realizado","Eliminado producto con exito")
    actualizarProducSuper(proListaSuper)
    actualizarProductosEliminados()
    boxDelProduc.set("")
    

def actualizarProducSuper(dicProductos):
    global producSuper
    listDelProduc = []
    for productosSuper in dicProductos:
        listDelProduc.append(f"{productosSuper["producto"]} - {productosSuper["precio"]}")
    
    producSuper = listDelProduc


def actualizarCompra(dicCompra):
    global compra
    listaCompra = []
    for producCompra in dicCompra:
        listaCompra.append(f"{producCompra["cantidad"]} - {producCompra["producto"]} - {producCompra["precio"]}")
    compra = listaCompra

def actualizarProductos():
    productos = productosSuper(producSuper)
    boxProductos['values'] = productos
    

def actualizarProductosEliminados():
    productos = productosSuper(producSuper)
    boxProductos['values'] = productos
    boxDelProduc['values'] = productos

def borraCompra():
    global compra
    compra = []
    imprimirCompra(compra)

def imprimirTicket():
    global compra
    fecha = datetime.now()
    productos = comprobarTicket(compra)
    totalCompra = precioTotal(compra)

    pdf = FPDF('P','cm','A5')
    #Salto de página
    pdf.set_auto_page_break(auto=True,margin=3)
    #agregar página
    pdf.add_page()
    #especificar fuente
    pdf.set_font('courier','U',16)

    pdf.cell(5,2,"Ticket de compra", ln=True)

    pdf.set_font('courier','',10)

    for producto in productos:
        listaCompra = f"nº:{producto["cantidad"]}  producto:{producto["producto"]}  precio:{producto["precio"]}"

        pdf.cell(0,1, listaCompra, ln=True)

    pdf.set_font('courier','B',10)
    pdf.cell(0,1, f"Total compra: {totalCompra}", ln=True)
    pdf.cell(0,1, f"Fecha de compra: {fecha.strftime('%Y-%m-%d')}", ln=True)

    pdf.output('ticket_compra.pdf')


#Interfaz gráfica
def interfazGrafica():

    root = Tk()

    root.title("Caja Registradora")
    root.resizable(1,1)

    miFrame = Frame(root, width=1000, height=550)
    miFrame.pack()

    labelCantidad = Label(miFrame, text = "Cantidad: ")
    labelCantidad.grid(row=0, column=0,sticky="w")

    labelProducto = Label(miFrame, text = "Producto: ")
    labelProducto.grid(row=1, column=0,sticky="w")

    labelPrecio = Label(miFrame, text = "Precio: ")
    labelPrecio.grid(row=2, column=0,sticky="w")

    global textoCantidad
    textoCantidad = Entry(miFrame)
    textoCantidad.grid(row=0,column=1,padx=30,pady=15)

    global precioProducto
    precioProducto = StringVar()

    global textoPrecio
    textoPrecio = Entry(miFrame, state="readonly", textvariable=precioProducto)
    textoPrecio.grid(row=2,column=1,padx=30,pady=15)

    productos = productosSuper(producSuper)
    global boxProductos
    boxProductos = ttk.Combobox(miFrame, values=productos)
    boxProductos.grid(row=1,column=1,padx=30,pady=15)
    boxProductos.config(state="readonly")
    boxProductos.bind("<<ComboboxSelected>>", actualizarPrecio)


    global textoCompra
    textoCompra = Text(miFrame, width=50, height=10)
    textoCompra.grid(row=3, columnspan=2, padx=10,pady=10)
   

    botonComprar = Button(root, text="Comprar", command=comprarProducto)
    botonComprar.pack()

    botonDeducProduc = Button(root, text="Deducir producto", command=descontarProducto)
    botonDeducProduc.pack()

    botonImpTicket = Button(root, text="Imprimir ticket", command=imprimirTicket)
    botonImpTicket.pack()

    botonDelCompra = Button(root, text="Borrar compra", command=borraCompra)
    botonDelCompra.pack()

    botonIntProdNew = Button(root, text="Introducir producto Supermercado", command=interfazProducNuevo)
    botonIntProdNew.pack()

    botonDelProdSuper = Button(root, text="Eliminar producto Supermercado", command=interfazDeleteProducto)
    botonDelProdSuper.pack()

    botonSalir = Button(root, text="Salir",  command=lambda: root.destroy())
    botonSalir.pack()

    root.mainloop()

def interfazProducNuevo():

    root02 = Tk()

    root02.title("Producto nuevo")
    root02.resizable(1,1)

    miFrame = Frame(root02, width=1000, height=550)
    miFrame.pack()

    labelProducNew = Label(miFrame, text = "Producto: ")
    labelProducNew.grid(row=1, column=0,sticky="w")

    labelPrecioNew = Label(miFrame, text = "Precio: ")
    labelPrecioNew.grid(row=2, column=0,sticky="w")

    global textoProducNew
    textoProducNew = Entry(miFrame, state="normal")
    textoProducNew.grid(row=1,column=1,padx=30,pady=15)

    global textoPrecioNew
    textoPrecioNew = Entry(miFrame, state="normal")
    textoPrecioNew.grid(row=2,column=1,padx=30,pady=15)

    botonNewProduct = Button(root02, text="Ingresar producto", command=ingresarProducto)
    botonNewProduct.pack()

    botonSalir = Button(root02, text="Salir", command=lambda: root02.destroy())
    botonSalir.pack()

    root02.mainloop()

def interfazDeleteProducto():

    root02 = Tk()

    root02.title("Eliminar producto")
    root02.resizable(1,1)

    miFrame = Frame(root02, width=1000, height=550)
    miFrame.pack()

    labelProduc = Label(miFrame, text = "Producto: ")
    labelProduc.grid(row=1, column=0,sticky="w")

    productos = productosSuper(producSuper)
    global boxDelProduc
    boxDelProduc = ttk.Combobox(miFrame, values=productos)
    boxDelProduc.grid(row=1,column=1,padx=30,pady=15)
    boxDelProduc.config(state="readonly")
    #boxProductos.bind("<<ComboboxSelected>>")

    botonDelProduct = Button(root02, text="Eliminar producto", command=delProducSuper)
    botonDelProduct.pack()

    botonSalir = Button(root02, text="Salir", command=lambda: root02.destroy())
    botonSalir.pack()

    root02.mainloop()


interfazGrafica()


