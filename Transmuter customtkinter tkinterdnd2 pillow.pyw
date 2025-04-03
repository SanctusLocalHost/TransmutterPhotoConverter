import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image

class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        # Modo escuro e tema
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.title("Transmuter Photo Converter")
        self.geometry("450x650")
        self.configure(bg="#2b2b2b")

        container = ctk.CTkFrame(self, corner_radius=10, fg_color="#2b2b2b")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Área de Drag & Drop
        self.drop_frame = ctk.CTkFrame(container, width=400, height=120, corner_radius=10, fg_color="#3b3b3b")
        self.drop_frame.pack(pady=10)
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.drop_event)

        self.drop_label = ctk.CTkLabel(
            self.drop_frame,
            text="Arrasta e solta as imagens aqui",
            fg_color="#3b3b3b",
            corner_radius=10
        )
        self.drop_label.place(relx=0.5, rely=0.5, anchor="center")

        import_button = ctk.CTkButton(container, text="Importar Imagens", command=self.importar_imagens)
        import_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(container, text="", fg_color="#2b2b2b")
        self.status_label.pack(pady=5)

        frame_resolucao = ctk.CTkFrame(container, corner_radius=10, fg_color="#3b3b3b")
        frame_resolucao.pack(pady=20, padx=20, fill="x")

        resolucao_label = ctk.CTkLabel(frame_resolucao, text="Defina a resolução (Largura x Altura):", fg_color="#3b3b3b")
        resolucao_label.pack(pady=5)

        self.largura_entry = ctk.CTkEntry(frame_resolucao, placeholder_text="Ex: 800")
        self.largura_entry.pack(pady=5, padx=10)

        self.altura_entry = ctk.CTkEntry(frame_resolucao, placeholder_text="Ex: 600")
        self.altura_entry.pack(pady=5, padx=10)

        frame_formato = ctk.CTkFrame(container, corner_radius=10, fg_color="#3b3b3b")
        frame_formato.pack(pady=20, padx=20, fill="x")

        formato_label = ctk.CTkLabel(frame_formato, text="Selecione o formato de saída:", fg_color="#3b3b3b")
        formato_label.pack(pady=5)

        # Adicionamos a opção "Manter Original" para que, se o usuário não quiser alterar o formato,
        # o programa mantenha a extensão original da imagem.
        formatos = ["Manter Original", "PNG", "JPEG", "JPG", "BMP", "GIF", "TIFF", "WEBP", "ICO"]
        self.formato_option = ctk.CTkOptionMenu(frame_formato, values=formatos)
        self.formato_option.set("Manter Original")
        self.formato_option.pack(pady=5, padx=10)

        converter_button = ctk.CTkButton(container, text="Converter Imagens", command=self.converter_imagens)
        converter_button.pack(pady=20)

        self.images_list = []

    def drop_event(self, event):
        raw_files = self.tk.splitlist(event.data)
        adicionou_arquivo = False

        for f in raw_files:
            f = f.strip()
            if f.startswith("{") and f.endswith("}"):
                f = f[1:-1]

            if os.path.isfile(f):
                self.images_list.append(f)
                adicionou_arquivo = True

        if adicionou_arquivo:
            self.status_label.configure(text="IMAGENS IMPORTADAS COM SUCESSO (drag & drop)!")
        else:
            self.status_label.configure(text="Nenhum arquivo detectado no drop...")

    def importar_imagens(self):
        arquivos = filedialog.askopenfilenames(
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.tiff;*.webp;*.ico")]
        )
        if arquivos:
            self.images_list.extend(arquivos)
            self.status_label.configure(text="IMAGENS IMPORTADAS COM SUCESSO!")
        else:
            self.status_label.configure(text="Nenhuma imagem foi importada.")

    def converter_imagens(self):
        if not self.images_list:
            messagebox.showerror("Erro", "Nenhuma imagem foi importada!")
            return

        # Verifica se o usuário informou resolução
        largura_text = self.largura_entry.get().strip()
        altura_text = self.altura_entry.get().strip()

        resolution_conversion = False
        largura = None
        altura = None

        if largura_text and altura_text:
            try:
                largura = int(largura_text)
                altura = int(altura_text)
                if largura <= 0 or altura <= 0:
                    raise ValueError
                resolution_conversion = True
            except ValueError:
                messagebox.showerror("Erro", "Insira uma resolução válida!")
                return

        # Verifica se o usuário deseja alterar o formato
        formato = self.formato_option.get()
        if formato == "Manter Original":
            format_conversion = False
        else:
            format_conversion = True
            # Se o usuário escolheu "JPG", convertemos internamente para "JPEG"
            if formato.upper() == "JPG":
                formato = "JPEG"

        pasta_saida = os.path.join(os.getcwd(), "imagens_convertidas")
        if not os.path.exists(pasta_saida):
            os.makedirs(pasta_saida)

        for caminho in self.images_list:
            try:
                img = Image.open(caminho)

                # Se for solicitado alteração de resolução, redimensiona a imagem
                if resolution_conversion:
                    img = img.resize((largura, altura), Image.Resampling.LANCZOS)

                # Se for solicitado alteração de formato, realiza a conversão
                if format_conversion:
                    if formato.upper() == "JPEG" and img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    new_ext = formato.lower()
                    new_format = formato
                else:
                    # Mantém o formato original da imagem
                    original_ext = os.path.splitext(caminho)[1][1:]  # remove o ponto
                    new_ext = original_ext.lower()
                    new_format = None  # Deixa que o Pillow determine

                nome_base = os.path.splitext(os.path.basename(caminho))[0]
                novo_nome = f"{nome_base}.{new_ext}"
                caminho_novo = os.path.join(pasta_saida, novo_nome)

                if format_conversion:
                    img.save(caminho_novo, format=new_format)
                else:
                    img.save(caminho_novo)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao converter {caminho}.\n{e}")
                return

        messagebox.showinfo("Sucesso", "Imagens convertidas com Sucesso!")
        self.images_list.clear()
        self.status_label.configure(text="")

if __name__ == "__main__":
    app = App()
    app.mainloop()
