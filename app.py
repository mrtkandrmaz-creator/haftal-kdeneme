import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os

DATA_FILE = "sinav_verileri.json"

class SinavMerkeziApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sınav Merkezi - Kullanıcı Değerlendirme Sistemi")
        self.root.geometry("900x650")
        self.root.config(bg="#f0f2f5")

        self.current_user = ""
        self.data = self.load_data()

        self.show_login_screen()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- 1. GİRİŞ EKRANI ---
    def show_login_screen(self):
        self.clear_window()

        frame = tk.Frame(self.root, bg="white", padx=40, pady=40, relief=tk.RAISED, borderwidth=1)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(frame, text="🎓 Sınav Merkezi Giriş", font=("Arial", 18, "bold"), bg="white", fg="#333").pack(pady=10)
        tk.Label(frame, text="Lütfen kullanıcı adınızı giriniz:", font=("Arial", 11), bg="white", fg="#666").pack(anchor=tk.W, pady=5)

        self.username_entry = tk.Entry(frame, font=("Arial", 14), width=25, relief=tk.SOLID, borderwidth=1)
        self.username_entry.pack(pady=10)
        self.username_entry.focus()
        self.username_entry.bind("<Return>", lambda event: self.login())

        btn = tk.Button(frame, text="Giriş Yap / Devam Et", font=("Arial", 12, "bold"), bg="#4a90e2", fg="white", relief=tk.FLAT, padx=10, pady=5, command=self.login)
        btn.pack(pady=15, fill=tk.X)

    def login(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Hata", "Kullanıcı adı boş olamaz!")
            return
        
        self.current_user = username
        if self.current_user not in self.data:
            self.data[self.current_user] = []

        self.show_main_dashboard()

    # --- 2. ANA PANEL & SINAV MERKEZİ ---
    def show_main_dashboard(self):
        self.clear_window()

        # Üst Bilgi Çubuğu
        top_bar = tk.Frame(self.root, bg="#2c3e50", height=60, padx=20)
        top_bar.pack(side=tk.TOP, fill=tk.X)

        tk.Label(top_bar, text=f"Hoş Geldiniz, {self.current_user} (Sınav Merkezi)", font=("Arial", 14, "bold"), bg="#2c3e50", fg="white").pack(side=tk.LEFT, pady=15)
        tk.Button(top_bar, text="Çıkış Yap", font=("Arial", 10), bg="#e74c3c", fg="white", relief=tk.FLAT, command=self.show_login_screen).pack(side=tk.RIGHT, pady=15)

        # Sekme (Notebook) Yapısı
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab_list = tk.Frame(notebook, bg="#f0f2f5")
        self.tab_add = tk.Frame(notebook, bg="#f0f2f5")
        self.tab_compare = tk.Frame(notebook, bg="#f0f2f5")
        self.tab_general = tk.Frame(notebook, bg="#f0f2f5")

        notebook.add(self.tab_list, text="📋 Sınavlarım & Tekil İnceleme")
        notebook.add(self.tab_add, text="➕ Yeni Sınav Ekle")
        notebook.add(self.tab_compare, text="⚖️️ Sınav Karşılaştırma")
        notebook.add(self.tab_general, text="📊 Genel Değerlendirme")

        self.setup_list_tab()
        self.setup_add_tab()
        self.setup_compare_tab()
        self.setup_general_tab()

    # Sınav Listesi ve Tekil İnceleme Sekmesi
    def setup_list_tab(self):
        for widget in self.tab_list.winfo_children():
            widget.destroy()

        tk.Label(self.tab_list, text="Yapılan Sınavların Listesi", font=("Arial", 12, "bold"), bg="#f0f2f5").pack(anchor=tk.W, padx=10, pady=10)

        columns = ("Sınav Adı", "Tarih", "Net / Puan", "Doğru", "Yanlış", "Boş")
        self.tree = ttk.Treeview(self.tab_list, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10)

        # Verileri doldur
        self.refresh_exam_list()

        btn_frame = tk.Frame(self.tab_list, bg="#f0f2f5")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(btn_frame, text="Seçilen Sınavı Detaylı İncele", bg="#3498db", fg="white", font=("Arial", 10, "bold"), command=self.show_exam_detail).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Seçilen Sınavı Sil", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), command=self.delete_exam).pack(side=tk.LEFT, padx=5)

    def refresh_exam_list(self):
        if hasattr(self, 'tree'):
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            user_exams = self.data.get(self.current_user, [])
            for idx, exam in enumerate(user_exams):
                self.tree.insert("", tk.END, iid=idx, values=(
                    exam.get("name"),
                    exam.get("date"),
                    exam.get("score"),
                    exam.get("correct"),
                    exam.get("wrong"),
                    exam.get("empty")
                ))

    def show_exam_detail(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen incelenecek bir sınav seçin!")
            return
        
        idx = int(selected[0])
        exam = self.data[self.current_user][idx]

        detail_win = tk.Toplevel(self.root)
        detail_win.title(f"Sınav Detayı: {exam['name']}")
        detail_win.geometry("400x350")
        detail_win.config(bg="white")

        tk.Label(detail_win, text=f"📄 {exam['name']}", font=("Arial", 14, "bold"), bg="white", fg="#2c3e50").pack(pady=15)
        
        details = [
            f"Tarih: {exam.get('date', 'Belirtilmemiş')}",
            f"Toplam Puan / Net: {exam.get('score')}",
            f"Doğru Sayısı: {exam.get('correct')}",
            f"Yanlış Sayısı: {exam.get('wrong')}",
            f"Boş Sayısı: {exam.get('empty')}",
            f"Notlar / Açıklama:\n{exam.get('notes', 'Yok')}"
        ]

        for d in details:
            tk.Label(detail_win, text=d, font=("Arial", 11), bg="white", anchor="w").pack(fill=tk.X, padx=30, pady=3)

    def delete_exam(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen silinecek bir sınav seçin!")
            return
        
        if messagebox.askyesno("Onay", "Seçilen sınavı silmek istediğinize emin misiniz?"):
            idx = int(selected[0])
            del self.data[self.current_user][idx]
            self.save_data()
            self.refresh_exam_list()
            self.setup_compare_tab()
            self.setup_general_tab()
            messagebox.showinfo("Başarılı", "Sınav silindi.")

    # --- 3. YENİ SINAV EKLEME SEKMESİ ---
    def setup_add_tab(self):
        for widget in self.tab_add.winfo_children():
            widget.destroy()

        form_frame = tk.Frame(self.tab_add, bg="white", padx=30, pady=30, relief=tk.RAISED, borderwidth=1)
        form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=500, height=450)

        tk.Label(form_frame, text="Yeni Sınav Sonucu Ekle", font=("Arial", 14, "bold"), bg="white", fg="#333").pack(pady=10)

        fields = [
            ("Sınav Adı (Örn: TYT Deneme 1)", "name"),
            ("Tarih (Örn: 01.10.2026)", "date"),
            ("Net / Puan", "score"),
            ("Doğru Sayısı", "correct"),
            ("Yanlış Sayısı", "wrong"),
            ("Boş Sayısı", "empty")
        ]

        self.entries = {}
        for label_text, key in fields:
            f = tk.Frame(form_frame, bg="white")
            f.pack(fill=tk.X, pady=5)
            tk.Label(f, text=label_text, font=("Arial", 10), bg="white", width=20, anchor="w").pack(side=tk.LEFT)
            e = tk.Entry(f, font=("Arial", 10), relief=tk.SOLID, borderwidth=1)
            e.pack(side=tk.RIGHT, expand=True, fill=tk.X)
            self.entries[key] = e

        tk.Button(form_frame, text="Sınavı Kaydet", font=("Arial", 11, "bold"), bg="#27ae60", fg="white", relief=tk.FLAT, command=self.save_exam).pack(pady=20, fill=tk.X)

    def save_exam(self):
        exam_data = {}
        for key, entry in self.entries.items():
            val = entry.get().strip()
            if not val and key in ["name", "score"]:
                messagebox.showerror("Hata", "Sınav adı ve Puan/Net alanları zorunludur!")
                return
            exam_data[key] = val

        self.data[self.current_user].append(exam_data)
        self.save_data()
        messagebox.showinfo("Başarılı", "Sınav başarıyla Sınav Merkezi'ne eklendi!")

        # Formu temizle
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        # Diğer sekmeleri güncelle
        self.refresh_exam_list()
        self.setup_compare_tab()
        self.setup_general_tab()

    # --- 4. SINAV KARŞILAŞTIRMA SEKMESİ ---
    def setup_compare_tab(self):
        for widget in self.tab_compare.winfo_children():
            widget.destroy()

        user_exams = self.data.get(self.current_user, [])
        if not user_exams:
            tk.Label(self.tab_compare, text="Karşılaştırma için henüz kayıtlı sınavınız bulunmuyor.", font=("Arial", 11), bg="#f0f2f5").pack(pady=50)
            return

        tk.Label(self.tab_compare, text="Sınav Karşılaştırma Paneli", font=("Arial", 12, "bold"), bg="#f0f2f5").pack(anchor=tk.W, padx=10, pady=10)

        select_frame = tk.Frame(self.tab_compare, bg="#f0f2f5")
        select_frame.pack(fill=tk.X, padx=10)

        tk.Label(select_frame, text="1. Sınav:", bg="#f0f2f5", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        exam_names = [e["name"] for e in user_exams]
        
        self.cb1 = ttk.Combobox(select_frame, values=exam_names, state="readonly", width=25)
        self.cb1.pack(side=tk.LEFT, padx=5)
        if exam_names: self.cb1.current(0)

        tk.Label(select_frame, text="2. Sınav:", bg="#f0f2f5", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.cb2 = ttk.Combobox(select_frame, values=exam_names, state="readonly", width=25)
        self.cb2.pack(side=tk.LEFT, padx=5)
        if len(exam_names) > 1: self.cb2.current(1)
        elif exam_names: self.cb2.current(0)

        tk.Button(select_frame, text="Karşılaştır", bg="#2980b9", fg="white", font=("Arial", 10, "bold"), command=self.run_comparison).pack(side=tk.LEFT, padx=15)

        self.compare_result_frame = tk.Frame(self.tab_compare, bg="white", relief=tk.RAISED, borderwidth=1)
        self.compare_result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=15)

    def run_comparison(self):
        for widget in self.compare_result_frame.winfo_children():
            widget.destroy()

        idx1 = self.cb1.current()
        idx2 = self.cb2.current()
        user_exams = self.data.get(self.current_user, [])

        if idx1 < 0 or idx2 < 0 or idx1 >= len(user_exams) or idx2 >= len(user_exams):
            return

        e1 = user_exams[idx1]
        e2 = user_exams[idx2]

        # Grafik oluşturma
        fig, ax = plt.subplots(figsize=(6, 3.5))
        categories = ['Puan/Net', 'Doğru', 'Yanlış', 'Boş']
        
        try:
            val1 = [float(e1.get('score', 0)), float(e1.get('correct', 0)), float(e1.get('wrong', 0)), float(e1.get('empty', 0))]
            val2 = [float(e2.get('score', 0)), float(e2.get('correct', 0)), float(e2.get('wrong', 0)), float(e2.get('empty', 0))]
        except ValueError:
            val1 = [0, 0, 0, 0]
            val2 = [0, 0, 0, 0]

        x = range(len(categories))
        width = 0.35

        ax.bar([i - width/2 for i in x], val1, width, label=e1['name'], color="#3498db")
        ax.bar([i + width/2 for i in x], val2, width, label=e2['name'], color="#e67e22")

        ax.set_ylabel('Değerler')
        ax.set_title('Sınav Karşılaştırması')
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.compare_result_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # --- 5. GENEL DEĞERLENDİRME SEKMESİ ---
    def setup_general_tab(self):
        for widget in self.tab_general.winfo_children():
            widget.destroy()

        user_exams = self.data.get(self.current_user, [])
        if not user_exams:
            tk.Label(self.tab_general, text="Genel değerlendirme için henüz kayıtlı sınavınız bulunmuyor.", font=("Arial", 11), bg="#f0f2f5").pack(pady=50)
            return

        tk.Label(self.tab_general, text="Genel Değerlendirme & Gelişim Grafiği", font=("Arial", 12, "bold"), bg="#f0f2f5").pack(anchor=tk.W, padx=10, pady=10)

        # Özet İstatistikler
        try:
            scores = [float(e.get('score', 0)) for e in user_exams]
            avg_score = sum(scores) / len(scores) if scores else 0
            max_score = max(scores) if scores else 0
        except:
            avg_score, max_score = 0, 0

        stats_frame = tk.Frame(self.tab_general, bg="white", padx=15, pady=10, relief=tk.RAISED, borderwidth=1)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(stats_frame, text=f"Toplam Sınav: {len(user_exams)}", font=("Arial", 10, "bold"), bg="white").pack(side=tk.LEFT, padx=15)
        tk.Label(stats_frame, text=f"Ortalama Puan/Net: {avg_score:.2f}", font=("Arial", 10, "bold"), bg="white", fg="#2980b9").pack(side=tk.LEFT, padx=15)
        tk.Label(stats_frame, text=f"En Yüksek Puan/Net: {max_score}", font=("Arial", 10, "bold"), bg="white", fg="#27ae60").pack(side=tk.LEFT, padx=15)

        # Çizgi Grafik (Gelişim Trendi)
        graph_frame = tk.Frame(self.tab_general, bg="white", relief=tk.RAISED, borderwidth=1)
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        fig, ax = plt.subplots(figsize=(7, 3.5))
        names = [e.get('name', f"Sınav {i+1}") for i, e in enumerate(user_exams)]
        
        try:
            y_vals = [float(e.get('score', 0)) for e in user_exams]
        except:
            y_vals = [0] * len(user_exams)

        ax.plot(names, y_vals, marker='o', color='#2ecc71', linewidth=2, markersize=8)
        ax.set_title("Zamana Göre Sınav Puan / Net Gelişimi")
        ax.set_ylabel("Puan / Net")
        plt.xticks(rotation=15, ha='right')
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = SinavMerkeziApp(root)
    root.mainloop()
