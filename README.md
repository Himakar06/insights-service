# 📊 Data Insights as a Service  

A powerful SaaS-style tool that lets you **upload a CSV file** and instantly get **automated insights**, **visualizations**, and a professional **dashboard PDF** — all with a single click.  

---

## 🎯 Problem It Solves  

Exploring datasets is often slow and repetitive. Business users and analysts face common challenges:  
- Spending hours cleaning and analyzing every new dataset  
- Writing code just to get basic summaries or visualizations  
- Struggling to create dashboards and reports quickly  

This tool solves those pain points by providing:  
✅ **Instant insights** with one click — no coding required  
✅ **Auto-generated visualizations** that reveal trends & patterns immediately  
✅ **Ready-to-share PDF reports** in seconds  
✅ **(Coming Soon)** AI-powered chatbot interface for asking questions like *“Which category drives the most revenue?”*  
✅ **Minimal effort, maximum value** — reduce hours of manual work to just a few seconds  

---

## 🛠️ Features  

| Feature | Description |  
|---------|-------------|  
| 📁 **Upload CSV** | Upload any CSV dataset to start instantly |  
| 📊 **Automated EDA** | Generate profiling reports (summary stats, distributions, correlations) |  
| 📈 **Smart Visualizations** | Auto-generate bar, pie, line, and correlation charts |  
| 📄 **Export Dashboard** | Save insights & visuals into a polished PDF |  
| 💬 **Ask Your Data (Coming Soon)** | Natural language Q&A with your dataset via LLM |  

---

## 🔍 How This Differs from Existing LLMs (ChatGPT, Claude, etc..)  

While tools like **ChatGPT** or **ClaudeAI** are excellent for conversation and code generation, they are **not optimized for automated dataset analysis**.  

Here’s what makes this project stand out:  
- ⚡ **One-Click Workflow** → Upload a CSV → get EDA, visualizations, and a PDF dashboard. No prompting required.  
- 🖼️ **Zero Prompt Engineering** → Unlike LLMs where results depend on how you phrase a query, this tool gives consistent and structured outputs.  
- 🎯 **Purpose-Built for Data Analysis** → Specialized for **exploratory data analysis and visualization**, instead of being a general chatbot.  
- 📊 **Structured & Repeatable** → Every dataset gets the same professional treatment, ensuring consistency.  
- 📄 **Export-Ready Dashboards** → Generates polished, shareable PDF reports instantly (something LLMs don’t offer by default).  

👉 In short: **ChatGPT/Claude are great for conversation. This tool is built for automation.** Analysts and business users don’t have to type a single prompt — just **upload and go**.  

---

## 📊 CSV Insights Dashboard  

<p align="center">  
  <img src="images/dashboard.png" alt="Dashboard Screenshot" width="600"/>  
  <img src="images/preview.png" alt="Visualization Preview" width="600"/>  
  <img src="images/pdf.png" alt="PDF Export Screenshot" width="600"/>  
</p>  

---

## 🧠 Tech Stack  

- **Frontend/UI** → [Streamlit](https://streamlit.io)  
- **Data Analysis** → Pandas, NumPy  
- **Auto EDA** → YDataProfiling  
- **Visualizations** → Plotly, Seaborn, Matplotlib  
- **PDF Export** → FPDF  
- **Future** → OpenAI/HuggingFace Transformers for LLM-powered chat  

---

## 🚀 Getting Started  

### 🔧 Installation  

```bash
git clone https://github.com/Himakar06/insights-service.git
cd insights-service
pip install -r requirements.txt
streamlit run src/app.py
