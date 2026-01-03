import face_recognition
import tkinter as tk
from tkinter import filedialog, messagebox, Scale, Frame, Label, Button, Toplevel, ttk
from PIL import Image, ImageTk, ImageDraw
import os
import numpy as np
import time
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ScrollableImage(ttk.Frame):
    def __init__(self, master, width=350, height=350, **kw):
        super().__init__(master, **kw)
        self.canvas = tk.Canvas(self, width=width, height=height, bg="#e9ecef")
        self.h_scroll = ttk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.v_scroll = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.h_scroll.grid(row=1, column=0, sticky='ew')
        self.v_scroll.grid(row=0, column=1, sticky='ns')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.img_id = None
        self.img_ref = None  # Keep reference

    def show_image(self, pil_image):
        self.img_ref = ImageTk.PhotoImage(pil_image)
        if self.img_id is None:
            self.img_id = self.canvas.create_image(0, 0, anchor='nw', image=self.img_ref)
        else:
            self.canvas.itemconfig(self.img_id, image=self.img_ref)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FaceMatch Pro")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.image1_path = ""
        self.image2_path = ""
        self.tolerance = 0.5
        self.history = []
        
        # Configuración de estilo
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", font=("Arial", 10), padding=6)
        self.style.configure("TLabel", background="#f0f0f0")
        self.style.configure("Title.TLabel", font=("Arial", 14, "bold"), foreground="#2c3e50")
        
        # Crear interfaz
        self.create_widgets()
        
        # Cargar icono
        try:
            self.root.iconbitmap("face_icon.ico")
        except:
            pass
    
    def create_widgets(self):
        # Frame principal con grid
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        ttk.Label(title_frame, text="FaceMatch Pro - Sistema de Reconocimiento Facial", 
                 style="Title.TLabel").pack()

        # Panel de parámetros
        param_frame = ttk.LabelFrame(main_frame, text="Parámetros de Comparación")
        param_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        ttk.Label(param_frame, text="Tolerancia:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.tolerance_scale = Scale(
            param_frame, from_=0.1, to=1.0, resolution=0.01, orient=tk.HORIZONTAL,
            length=300, command=self.update_tolerance, highlightthickness=0, sliderrelief=tk.FLAT
        )
        self.tolerance_scale.set(self.tolerance)
        self.tolerance_scale.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        self.tolerance_value = ttk.Label(param_frame, text=f"Valor actual: {self.tolerance:.2f}")
        self.tolerance_value.grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(param_frame, text="Ver Historial", command=self.show_history).grid(
            row=0, column=3, padx=10, pady=5, sticky="e"
        )
        param_frame.grid_columnconfigure(1, weight=1)

        # Panel de imágenes
        img_frame = ttk.Frame(main_frame)
        img_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        main_frame.grid_rowconfigure(2, weight=1)

        # Imagen 1 con scroll y botón abajo
        img1_frame = ttk.LabelFrame(img_frame, text="Imagen 1", width=400, height=350)
        img1_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        img1_inner = ttk.Frame(img1_frame)
        img1_inner.grid(row=0, column=0, sticky="nsew")
        img1_frame.grid_rowconfigure(0, weight=1)
        img1_frame.grid_columnconfigure(0, weight=1)

        self.scroll_img1 = ScrollableImage(img1_inner, width=350, height=300)
        self.scroll_img1.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))
        btn_img1 = ttk.Button(img1_inner, text="Seleccionar Imagen 1", command=lambda: self.load_image(1))
        btn_img1.grid(row=1, column=0, pady=(10, 10), sticky="ew")

        img1_inner.grid_rowconfigure(0, weight=1)
        img1_inner.grid_columnconfigure(0, weight=1)

        # Imagen 2 con scroll y botón abajo
        img2_frame = ttk.LabelFrame(img_frame, text="Imagen 2", width=400, height=350)
        img2_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        img2_inner = ttk.Frame(img2_frame)
        img2_inner.grid(row=0, column=0, sticky="nsew")
        img2_frame.grid_rowconfigure(0, weight=1)
        img2_frame.grid_columnconfigure(0, weight=1)

        self.scroll_img2 = ScrollableImage(img2_inner, width=350, height=300)
        self.scroll_img2.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))
        btn_img2 = ttk.Button(img2_inner, text="Seleccionar Imagen 2", command=lambda: self.load_image(2))
        btn_img2.grid(row=1, column=0, pady=(10, 10), sticky="ew")

        img2_inner.grid_rowconfigure(0, weight=1)
        img2_inner.grid_columnconfigure(0, weight=1)

        img_frame.grid_columnconfigure(0, weight=1)
        img_frame.grid_columnconfigure(1, weight=1)
        img_frame.grid_rowconfigure(0, weight=1)

        # Panel de resultados
        result_frame = ttk.LabelFrame(main_frame, text="Resultados")
        result_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)
        self.progress = ttk.Progressbar(result_frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress.pack(pady=5, padx=10, fill=tk.X)
        self.lbl_similarity = ttk.Label(result_frame, text="", font=("Arial", 12))
        self.lbl_similarity.pack(pady=(10, 5))
        self.lbl_result = ttk.Label(result_frame, text="", font=("Arial", 14, "bold"))
        self.lbl_result.pack(pady=(0, 10))
        self.fig, self.ax = plt.subplots(figsize=(5, 2))
        self.canvas = FigureCanvasTkAgg(self.fig, master=result_frame)
        self.canvas.get_tk_widget().pack(fill=tk.X, padx=10, pady=10)
        self.ax.set_title('Distancia Facial')
        self.ax.set_ylim(0, 1)

        # Botones de acción (siempre abajo)
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)
        self.btn_compare = ttk.Button(
            action_frame, text="Comparar Rostros", command=self.compare_faces, state=tk.DISABLED, style="Accent.TButton"
        )
        self.btn_compare.pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Guardar Resultados", command=self.save_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Reiniciar", command=self.reset_app).pack(side=tk.RIGHT, padx=5)
        self.style.configure("Accent.TButton", background="#3498db", foreground="white")

    def update_tolerance(self, value):
        self.tolerance = float(value)
        self.tolerance_value.config(text=f"Valor actual: {self.tolerance:.2f}")
    
    def load_image(self, image_num):
        file_path = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png")]
        )
        if not file_path:
            return
        try:
            img = Image.open(file_path)
            img_with_faces = self.detect_and_draw_faces(np.array(img.copy()))
            pil_img = Image.fromarray(img_with_faces)
            if image_num == 1:
                self.image1_path = file_path
                self.scroll_img1.show_image(pil_img)
            else:
                self.image2_path = file_path
                self.scroll_img2.show_image(pil_img)
            if self.image1_path and self.image2_path:
                self.btn_compare.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")

    
    def detect_and_draw_faces(self, image):
        # Detectar ubicaciones de rostros
        face_locations = face_recognition.face_locations(image)
        
        # Dibujar cuadros alrededor de cada rostro
        for top, right, bottom, left in face_locations:
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        
        return image
    
    def compare_faces(self):
        if not self.image1_path or not self.image2_path:
            messagebox.showwarning("Advertencia", "Seleccione ambas imágenes primero")
            return
            
        try:
            # Iniciar barra de progreso
            self.progress['value'] = 0
            self.root.update()
            
            # Cargar imágenes
            self.progress['value'] = 20
            img1 = face_recognition.load_image_file(self.image1_path)
            img2 = face_recognition.load_image_file(self.image2_path)
            
            # Detectar rostros
            self.progress['value'] = 40
            encodings1 = face_recognition.face_encodings(img1)
            encodings2 = face_recognition.face_encodings(img2)
            
            # Validar rostros detectados
            self.progress['value'] = 60
            if not encodings1:
                messagebox.showerror("Error", "No se detectaron rostros en la Imagen 1")
                return
                
            if not encodings2:
                messagebox.showerror("Error", "No se detectaron rostros en la Imagen 2")
                return
            
            # Calcular distancia facial
            self.progress['value'] = 80
            distance = face_recognition.face_distance([encodings1[0]], encodings2[0])[0]
            similarity = (1 - distance) * 100
            
            # Comparar con tolerancia
            result = distance <= self.tolerance
            
            # Actualizar gráfico
            self.update_similarity_chart(distance)
            
            # Mostrar resultados
            color = "green" if result else "red"
            self.lbl_similarity.config(
                text=f"Similitud: {similarity:.2f}% | Distancia: {distance:.4f} | Tolerancia: {self.tolerance:.2f}",
                foreground=color
            )
            
            result_text = "✅ Misma persona" if result else "❌ Personas diferentes"
            self.lbl_result.config(text=result_text, foreground=color)
            
            # Guardar en historial
            self.history.append({
                "image1": self.image1_path,
                "image2": self.image2_path,
                "distance": distance,
                "similarity": similarity,
                "result": result,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            self.progress['value'] = 100
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al comparar rostros: {str(e)}")
    
    def update_similarity_chart(self, distance):
        self.ax.clear()
        
        # Crear barras
        bars = self.ax.bar(['Distancia', 'Tolerancia'], [distance, self.tolerance], 
                          color=['#e74c3c', '#3498db'])
        
        # Añadir valores encima de las barras
        for bar in bars:
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.2f}', ha='center', va='bottom')
        
        # Línea de umbral
        self.ax.axhline(y=self.tolerance, color='#2c3e50', linestyle='--', alpha=0.7)
        
        self.ax.set_ylim(0, 1)
        self.ax.set_title('Comparación Facial')
        self.canvas.draw()
    
    def show_history(self):
        if not self.history:
            messagebox.showinfo("Historial", "No hay comparaciones registradas")
            return
            
        history_win = Toplevel(self.root)
        history_win.title("Historial de Comparaciones")
        history_win.geometry("800x500")
        
        # Crear tabla
        columns = ("#", "Fecha", "Imagen 1", "Imagen 2", "Distancia", "Resultado")
        tree = ttk.Treeview(history_win, columns=columns, show="headings")
        
        # Configurar columnas
        tree.heading("#", text="#")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Imagen 1", text="Imagen 1")
        tree.heading("Imagen 2", text="Imagen 2")
        tree.heading("Distancia", text="Distancia")
        tree.heading("Resultado", text="Resultado")
        
        tree.column("#", width=50, anchor=tk.CENTER)
        tree.column("Fecha", width=150)
        tree.column("Imagen 1", width=150)
        tree.column("Imagen 2", width=150)
        tree.column("Distancia", width=100, anchor=tk.CENTER)
        tree.column("Resultado", width=100, anchor=tk.CENTER)
        
        # Añadir datos
        for i, item in enumerate(reversed(self.history), 1):
            result = "Misma persona" if item["result"] else "Diferente"
            tree.insert("", tk.END, values=(
                i,
                item["timestamp"],
                os.path.basename(item["image1"]),
                os.path.basename(item["image2"]),
                f"{item['distance']:.4f}",
                result
            ))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botón para exportar
        ttk.Button(history_win, text="Exportar a CSV", 
                  command=lambda: self.export_to_csv()).pack(pady=10)
    
    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'w') as f:
                f.write("Fecha,Imagen1,Imagen2,Distancia,Similitud(%),Resultado\n")
                for item in self.history:
                    result = "Misma persona" if item["result"] else "Personas diferentes"
                    f.write(f"{item['timestamp']},{os.path.basename(item['image1'])},"
                            f"{os.path.basename(item['image2'])},{item['distance']:.4f},"
                            f"{item['similarity']:.2f},{result}\n")
            messagebox.showinfo("Éxito", "Historial exportado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")
    
    def save_results(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'w') as f:
                f.write("Resultado de Comparación Facial\n")
                f.write("="*40 + "\n\n")
                f.write(f"Imagen 1: {os.path.basename(self.image1_path)}\n")
                f.write(f"Imagen 2: {os.path.basename(self.image2_path)}\n\n")
                f.write(f"Tolerancia usada: {self.tolerance:.2f}\n")
                f.write(f"Distancia facial: {distance:.4f}\n")
                f.write(f"Similitud: {similarity:.2f}%\n")
                f.write(f"Resultado: {'Misma persona' if result else 'Personas diferentes'}\n")
            messagebox.showinfo("Éxito", "Resultados guardados correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")
    
    def reset_app(self):
        self.image1_path = ""
        self.image2_path = ""
        self.lbl_img1.config(image="", text="Imagen no seleccionada")
        self.lbl_img2.config(image="", text="Imagen no seleccionada")
        self.lbl_similarity.config(text="")
        self.lbl_result.config(text="")
        self.progress['value'] = 0
        self.ax.clear()
        self.canvas.draw()
        self.btn_compare.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
