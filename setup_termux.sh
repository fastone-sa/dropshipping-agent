#!/data/data/com.termux/files/usr/bin/bash
# سكربت إعداد مشروع Dropshipping AI Agent على Termux

# تحديث الحزم
pkg update -y && pkg upgrade -y

# تثبيت الأدوات الأساسية
pkg install -y git python nano

# إعداد مجلد المشروع
mkdir -p ~/dropshipping-agent
cd ~/dropshipping-agent

# تهيئة Git
git init

# إضافة الملفات (تأكد أنك وضعت agent.html, app.py, requirements.txt, Dockerfile, render.yaml, Procfile, README.md, .github/workflows/deploy.yml في هذا المجلد)
git add .
git commit -m "Initial commit - Dropshipping AI Agent"

# ربط المستودع على حسابك fastone-sa
git remote add origin https://github.com/fastone-sa/dropshipping-agent.git

# دفع الكود إلى الفرع الرئيسي
git branch -M main
git push -u origin main

echo "✅ تم رفع المشروع إلى GitHub: https://github.com/fastone-sa/dropshipping-agent"
echo "⚙️ الآن أضف الأسرار (Secrets) في إعدادات المستودع لتفعيل CI/CD."