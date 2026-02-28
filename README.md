# WorkSense AI - HR Analytics Dashboard

![WorkSense AI](https://img.shields.io/badge/WorkSense-AI-00d4ff?style=for-the-badge)
![React](https://img.shields.io/badge/React-18.2.0-61dafb?style=for-the-badge&logo=react)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Modern SaaS HR Analytics Dashboard with Dark Theme, Neon Blue Accents, and Enterprise Features.

## 🚀 Quick Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/rahul700raj/worksense-ai-dashboard)
[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/rahul700raj/worksense-ai-dashboard)

## 🌟 Features

### 🎯 Multi-Role Dashboards
- **HR Admin Dashboard** - Complete workforce overview with KPIs, charts, and analytics
- **Manager Dashboard** - Team performance tracking and project insights
- **Employee Dashboard** - Personal metrics, goals, and career development

### 🤖 AI-Powered Analytics
- **AI Insights** - Machine learning predictions and recommendations
- **Attrition Risk Analysis** - Predict and prevent employee turnover
- **Skill Gap Analysis** - Identify training needs and development opportunities

### 📊 Data Visualization
- Real-time animated charts using Recharts
- Interactive KPI cards with trend indicators
- Department distribution pie charts
- Performance trend line graphs
- Task distribution bar charts

### 🎨 Modern Design
- **Dark Theme** with Neon Blue accents
- **Corporate + Futuristic** aesthetic
- Glassmorphism effects
- Smooth animations and transitions
- Responsive mobile-first design

### 🔐 Authentication
- Multi-role login system
- Secure signup flow
- Role-based access control

## 📸 Screenshots

### Login Screen
Beautiful split-screen design with branding and features showcase.

### HR Admin Dashboard
Comprehensive workforce analytics with KPIs, headcount trends, and department distribution.

### AI Insights
Machine learning predictions for hiring, performance, and retention strategies.

### Attrition Risk
AI-powered employee retention risk analysis with actionable insights.

## 🛠️ Tech Stack

- **Frontend**: React 18.2.0
- **Charts**: Recharts 2.5.0
- **Styling**: CSS3 with custom animations
- **Build Tool**: Create React App
- **Deployment**: Vercel, Netlify, GitHub Pages

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/rahul700raj/worksense-ai-dashboard.git

# Navigate to project directory
cd worksense-ai-dashboard

# Install dependencies
npm install

# Start development server
npm start
```

The app will open at [http://localhost:3000](http://localhost:3000)

## 🏗️ Build for Production

```bash
# Create optimized production build
npm run build

# The build folder will contain optimized files ready for deployment
```

## 📱 Demo Credentials

Simply select your role and click "Sign In":
- **HR Admin** - Full access to all analytics and insights
- **Manager** - Team management and performance tracking
- **Employee** - Personal dashboard and career development

## 🎨 Design System

### Color Palette
- **Primary**: `#00d4ff` (Neon Blue)
- **Secondary**: `#0099cc` (Deep Blue)
- **Background**: `#0a0e27` (Dark Navy)
- **Surface**: `#1a1f3a` (Dark Blue)
- **Text**: `#ffffff` (White)
- **Muted**: `#8b92b0` (Gray Blue)

### Typography
- **Font Family**: Inter
- **Weights**: 300, 400, 500, 600, 700, 800

### Components
- Glassmorphism cards with backdrop blur
- Gradient buttons with hover effects
- Animated KPI cards with trend indicators
- Responsive sidebar navigation
- Interactive charts with tooltips

## 📊 Dashboard Screens

1. **Login / Signup** - Secure authentication with role selection
2. **HR Admin Dashboard** - Workforce overview, KPIs, charts
3. **Manager Dashboard** - Team performance and task distribution
4. **Employee Dashboard** - Personal metrics and goals
5. **AI Insights Page** - ML predictions and recommendations
6. **Attrition Risk Page** - Employee retention analytics
7. **Skill Gap Analysis Page** - Training needs identification

## 🌐 Deployment Options

### Vercel (Recommended)
```bash
npm install -g vercel
vercel login
vercel
```

### Netlify
```bash
npm install -g netlify-cli
netlify login
npm run build
netlify deploy --prod --dir=build
```

### GitHub Pages
```bash
npm install --save-dev gh-pages
# Add to package.json: "homepage": "https://yourusername.github.io/worksense-ai-dashboard"
npm run deploy
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 🎯 Use Cases

Perfect for:
- **Enterprise IT Companies** - Large-scale workforce analytics
- **HR Departments** - Data-driven decision making
- **Startups** - Modern HR management
- **Consulting Firms** - Client presentations
- **Educational Institutions** - HR analytics demonstrations

## 🔧 Customization

### Modify Theme Colors
Edit `src/App.css` and component CSS files to change colors:
```css
/* Primary color */
--primary: #00d4ff;

/* Background */
--background: #0a0e27;
```

### Add New Charts
Import Recharts components and add to dashboard:
```javascript
import { AreaChart, Area } from 'recharts';
```

### Extend Dashboards
Add new pages in `src/components/` and update routing in `App.js`

## 📈 Performance

- **Lighthouse Score**: 95+
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3s
- **Bundle Size**: Optimized with code splitting

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Rahul Mishra**
- Email: rm2778643@gmail.com
- GitHub: [@rahul700raj](https://github.com/rahul700raj)

## 🙏 Acknowledgments

- Design inspiration from modern SaaS dashboards
- Recharts for beautiful data visualization
- React community for excellent tools and libraries

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on [GitHub](https://github.com/rahul700raj/worksense-ai-dashboard/issues)
- Email: rm2778643@gmail.com

---

**⭐ Star this repository if you find it helpful!**

Made with ❤️ for modern HR analytics
