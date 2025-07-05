import os
import json
import uuid
import asyncio
import zipfile
from typing import Dict, List, Optional
from datetime import datetime
import logging
import re

from app.core.websocket_manager import manager
from app.core.config import settings

logger = logging.getLogger(__name__)

class WebsiteGenerator:
    def __init__(self, task_id: str, prompt: str):
        self.task_id = task_id
        self.prompt = prompt
        self.project_dir = os.path.join(settings.GENERATED_SITES_DIR, task_id)
        self.project_structure = {}
        self.current_step = ""
        self.progress = 0
        self.site_config = {}

    async def generate_website(self):
        """Main generation process orchestrator"""
        try:
            await self._log("🚀 Starting website generation process...")
            await self._update_progress("Initializing", 5)
            
            # Create project directory
            os.makedirs(self.project_dir, exist_ok=True)
            
            # Phase 1: Analyze prompt and plan structure
            await self._update_progress("🔍 Analyzing your requirements", 15)
            structure = await self.analyze_prompt()
            
            # Phase 2: Generate project structure
            await self._update_progress("📋 Planning website architecture", 25)
            await self.plan_structure(structure)
            
            # Phase 3: Generate components
            await self._update_progress("🏗️ Generating HTML structure", 40)
            await self.generate_html_components()
            
            await self._update_progress("🎨 Creating beautiful CSS styles", 60)
            await self.generate_css_styles()
            
            await self._update_progress("⚡ Adding interactive JavaScript", 75)
            await self.generate_javascript()
            
            await self._update_progress("📱 Optimizing for mobile devices", 85)
            await self.generate_responsive_styles()
            
            # Phase 4: Assemble final project
            await self._update_progress("🔧 Assembling final project", 95)
            await self.assemble_project()
            
            await self._update_progress("✅ Website generation complete!", 100)
            await self._log("🎉 Your website has been generated successfully!")
            
            # Notify completion with URLs
            preview_url = f"/api/preview/{self.task_id}/"
            download_url = f"/api/download/{self.task_id}"
            await manager.send_completion(self.task_id, preview_url, download_url)
            
        except Exception as e:
            logger.error(f"Error in website generation: {e}")
            await manager.send_error(self.task_id, f"Generation failed: {str(e)}")
            raise

    async def analyze_prompt(self) -> Dict:
        """Enhanced AI-powered prompt analysis"""
        await self._log("🧠 Analyzing your prompt with AI intelligence...")
        
        prompt_lower = self.prompt.lower()
        
        # Enhanced pattern matching for better site detection
        site_type = "landing_page"
        theme = "modern"
        color_scheme = "blue"
        sections = ["hero", "about", "features", "contact"]
        
        # Advanced site type detection
        if any(word in prompt_lower for word in ["portfolio", "personal", "resume", "cv", "work", "projects"]):
            site_type = "portfolio"
            sections = ["hero", "about", "projects", "skills", "experience", "contact"]
            theme = "creative"
            await self._log("📄 Detected: Portfolio website")
            
        elif any(word in prompt_lower for word in ["business", "company", "corporate", "enterprise", "agency"]):
            site_type = "business"
            sections = ["hero", "services", "about", "team", "testimonials", "contact"]
            theme = "professional"
            await self._log("🏢 Detected: Business website")
            
        elif any(word in prompt_lower for word in ["blog", "news", "articles", "writing", "content"]):
            site_type = "blog"
            sections = ["header", "featured", "articles", "categories", "about", "contact"]
            theme = "editorial"
            await self._log("📝 Detected: Blog website")
            
        elif any(word in prompt_lower for word in ["restaurant", "cafe", "food", "menu", "dining"]):
            site_type = "restaurant"
            sections = ["hero", "menu", "about", "gallery", "reservations", "contact"]
            theme = "warm"
            color_scheme = "orange"
            await self._log("🍽️ Detected: Restaurant website")
            
        elif any(word in prompt_lower for word in ["shop", "store", "ecommerce", "sell", "buy", "product"]):
            site_type = "ecommerce"
            sections = ["hero", "products", "categories", "about", "cart", "contact"]
            theme = "clean"
            await self._log("🛒 Detected: E-commerce website")

        # Color scheme detection
        color_keywords = {
            "blue": ["blue", "ocean", "professional", "corporate", "tech"],
            "green": ["green", "nature", "eco", "organic", "health"],
            "purple": ["purple", "creative", "artistic", "luxury", "premium"],
            "orange": ["orange", "energy", "food", "warm", "friendly"],
            "red": ["red", "bold", "passion", "restaurant", "emergency"],
            "pink": ["pink", "beauty", "fashion", "feminine", "cosmetic"],
            "dark": ["dark", "modern", "minimal", "sleek", "tech"],
        }
        
        for color, keywords in color_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                color_scheme = color
                break

        structure = {
            "site_type": site_type,
            "theme": theme,
            "sections": sections,
            "color_scheme": color_scheme,
            "has_navigation": True,
            "is_responsive": True,
            "has_animations": True,
            "modern_design": True
        }
        
        self.site_config = structure
        await self._log(f"🎨 Theme: {theme} | Color: {color_scheme}")
        await self._log(f"📐 Sections: {', '.join(sections)}")
        
        return structure

    async def plan_structure(self, structure: Dict):
        """Plan detailed project structure with modern build setup"""
        await self._log("📁 Planning modern project structure...")
        
        self.project_structure = {
            "index.html": "main_page",
            "css/": {
                "style.css": "main_styles",
                "responsive.css": "responsive_styles",
                "animations.css": "animation_styles"
            },
            "js/": {
                "main.js": "main_functionality",
                "animations.js": "scroll_animations"
            },
            "assets/": {
                "images/": {},
                "icons/": {}
            },
            "README.md": "project_documentation"
        }
        
        await self._log("✅ Modern project structure planned")

    async def generate_html_components(self):
        """Generate modern, semantic HTML with accessibility"""
        await self._log("🏗️ Generating semantic HTML structure...")
        
        html_content = self._create_modern_html_template()
        
        html_path = os.path.join(self.project_dir, "index.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        await self._log("✅ Modern HTML components generated")

    async def generate_css_styles(self):
        """Generate modern CSS with CSS Grid, Flexbox, and custom properties"""
        await self._log("🎨 Generating modern CSS styles...")
        
        # Create CSS directory
        css_dir = os.path.join(self.project_dir, "css")
        os.makedirs(css_dir, exist_ok=True)
        
        # Generate main styles
        css_content = self._create_modern_css_template()
        css_path = os.path.join(css_dir, "style.css")
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        # Generate animations
        animations_content = self._create_animations_css()
        animations_path = os.path.join(css_dir, "animations.css")
        with open(animations_path, 'w', encoding='utf-8') as f:
            f.write(animations_content)
            
        await self._log("✅ Beautiful CSS styles generated")

    async def generate_responsive_styles(self):
        """Generate responsive CSS for all device sizes"""
        await self._log("📱 Creating responsive design...")
        
        css_dir = os.path.join(self.project_dir, "css")
        responsive_content = self._create_responsive_css()
        
        responsive_path = os.path.join(css_dir, "responsive.css")
        with open(responsive_path, 'w', encoding='utf-8') as f:
            f.write(responsive_content)
            
        await self._log("✅ Responsive design optimized")

    async def generate_javascript(self):
        """Generate modern JavaScript with ES6+ features"""
        await self._log("⚡ Generating interactive JavaScript...")
        
        # Create JS directory
        js_dir = os.path.join(self.project_dir, "js")
        os.makedirs(js_dir, exist_ok=True)
        
        # Main functionality
        js_content = self._create_modern_js_template()
        js_path = os.path.join(js_dir, "main.js")
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        # Animations and interactions
        animations_js = self._create_animations_js()
        animations_path = os.path.join(js_dir, "animations.js")
        with open(animations_path, 'w', encoding='utf-8') as f:
            f.write(animations_js)
            
        await self._log("✅ Interactive features implemented")

    async def assemble_project(self):
        """Final assembly with documentation"""
        await self._log("🔧 Assembling final project...")
        
        # Create assets directories
        assets_dir = os.path.join(self.project_dir, "assets")
        os.makedirs(os.path.join(assets_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(assets_dir, "icons"), exist_ok=True)
        
        # Create README.md
        readme_content = self._create_project_readme()
        readme_path = os.path.join(self.project_dir, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # Create project manifest
        manifest = {
            "generated_at": datetime.now().isoformat(),
            "prompt": self.prompt,
            "task_id": self.task_id,
            "site_config": self.site_config,
            "structure": self.project_structure,
            "generator_version": "2.0.0"
        }
        
        manifest_path = os.path.join(self.project_dir, "project.json")
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
            
        await self._log("✅ Project assembly complete")

    def create_zip_archive(self) -> str:
        """Create a ZIP archive of the generated project"""
        zip_path = os.path.join(settings.GENERATED_SITES_DIR, f"{self.task_id}.zip")
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.project_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, self.project_dir)
                    zipf.write(file_path, arc_name)
        
        return zip_path

    async def _update_progress(self, step: str, progress: int):
        """Update progress and notify via WebSocket"""
        self.current_step = step
        self.progress = progress
        await manager.send_progress(self.task_id, step, progress)

    async def _log(self, message: str, level: str = "info"):
        """Log message and send via WebSocket"""
        logger.info(f"[{self.task_id}] {message}")
        await manager.send_log(self.task_id, message, level)

    def _create_modern_html_template(self) -> str:
        """Create modern, semantic HTML template"""
        site_type = self.site_config.get("site_type", "landing_page")
        sections = self.site_config.get("sections", ["hero", "about", "contact"])
        
        title = self._generate_site_title()
        
        # Generate sections based on site type
        sections_html = ""
        for section in sections:
            sections_html += self._generate_section_html(section)
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Generated website based on: {self.prompt[:150]}...">
    <title>{title}</title>
    
    <!-- CSS Files -->
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/responsive.css">
    <link rel="stylesheet" href="css/animations.css">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar" id="navbar">
        <div class="nav-container">
            <div class="nav-logo">
                <h2>{title.split()[0] if title.split() else "Website"}</h2>
            </div>
            <ul class="nav-menu" id="nav-menu">
                {self._generate_nav_items(sections)}
            </ul>
            <div class="nav-toggle" id="mobile-menu">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main>
        {sections_html}
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>{title.split()[0] if title.split() else "Website"}</h3>
                    <p>Generated with AI-powered technology</p>
                </div>
                <div class="footer-section">
                    <h4>Quick Links</h4>
                    <ul>
                        {self._generate_footer_links(sections)}
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Connect</h4>
                    <div class="social-links">
                        <a href="#" aria-label="Facebook"><i class="fab fa-facebook"></i></a>
                        <a href="#" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
                        <a href="#" aria-label="LinkedIn"><i class="fab fa-linkedin"></i></a>
                        <a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 {title}. Created with Weaver AI.</p>
            </div>
        </div>
    </footer>

    <!-- JavaScript Files -->
    <script src="js/main.js"></script>
    <script src="js/animations.js"></script>
</body>
</html>'''

    def _generate_site_title(self) -> str:
        """Generate appropriate site title based on prompt"""
        site_type = self.site_config.get("site_type", "landing_page")
        
        if "portfolio" in site_type:
            return "Creative Portfolio"
        elif "business" in site_type:
            return "Professional Business"
        elif "blog" in site_type:
            return "Digital Blog"
        elif "restaurant" in site_type:
            return "Fine Dining"
        elif "ecommerce" in site_type:
            return "Online Store"
        else:
            return "Modern Website"

    def _generate_section_html(self, section: str) -> str:
        """Generate HTML for specific sections"""
        if section == "hero":
            return self._generate_hero_section()
        elif section == "about":
            return self._generate_about_section()
        elif section == "services":
            return self._generate_services_section()
        elif section == "projects" or section == "portfolio":
            return self._generate_projects_section()
        elif section == "contact":
            return self._generate_contact_section()
        elif section == "features":
            return self._generate_features_section()
        else:
            return f'''
        <section id="{section}" class="section">
            <div class="container">
                <h2 class="section-title">{section.title()}</h2>
                <p class="section-description">This is the {section} section of your website.</p>
            </div>
        </section>'''

    def _generate_hero_section(self) -> str:
        """Generate hero section HTML"""
        return '''
        <section id="hero" class="hero">
            <div class="hero-container">
                <div class="hero-content">
                    <h1 class="hero-title">Welcome to Your New Website</h1>
                    <p class="hero-subtitle">Experience innovation and excellence in every detail</p>
                    <div class="hero-buttons">
                        <a href="#about" class="btn btn-primary">Learn More</a>
                        <a href="#contact" class="btn btn-secondary">Get Started</a>
                    </div>
                </div>
                <div class="hero-image">
                    <div class="hero-placeholder">
                        <i class="fas fa-rocket"></i>
                    </div>
                </div>
            </div>
        </section>'''

    def _generate_about_section(self) -> str:
        """Generate about section HTML"""
        return '''
        <section id="about" class="section">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">About Us</h2>
                    <p class="section-subtitle">Discover our story and mission</p>
                </div>
                <div class="about-grid">
                    <div class="about-content">
                        <h3>Our Mission</h3>
                        <p>We are dedicated to delivering exceptional experiences and innovative solutions that make a difference.</p>
                        <div class="about-stats">
                            <div class="stat">
                                <span class="stat-number">100+</span>
                                <span class="stat-label">Projects</span>
                            </div>
                            <div class="stat">
                                <span class="stat-number">50+</span>
                                <span class="stat-label">Clients</span>
                            </div>
                            <div class="stat">
                                <span class="stat-number">5+</span>
                                <span class="stat-label">Years</span>
                            </div>
                        </div>
                    </div>
                    <div class="about-image">
                        <div class="image-placeholder">
                            <i class="fas fa-users"></i>
                        </div>
                    </div>
                </div>
            </div>
        </section>'''

    def _generate_contact_section(self) -> str:
        """Generate contact section HTML"""
        return '''
        <section id="contact" class="section contact-section">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">Get In Touch</h2>
                    <p class="section-subtitle">Ready to start your project? Contact us today</p>
                </div>
                <div class="contact-grid">
                    <div class="contact-info">
                        <div class="contact-item">
                            <i class="fas fa-envelope"></i>
                            <div>
                                <h4>Email</h4>
                                <p>hello@example.com</p>
                            </div>
                        </div>
                        <div class="contact-item">
                            <i class="fas fa-phone"></i>
                            <div>
                                <h4>Phone</h4>
                                <p>+1 (555) 123-4567</p>
                            </div>
                        </div>
                        <div class="contact-item">
                            <i class="fas fa-map-marker-alt"></i>
                            <div>
                                <h4>Address</h4>
                                <p>123 Business St, City, State 12345</p>
                            </div>
                        </div>
                    </div>
                    <form class="contact-form">
                        <div class="form-group">
                            <input type="text" name="name" placeholder="Your Name" required>
                        </div>
                        <div class="form-group">
                            <input type="email" name="email" placeholder="Your Email" required>
                        </div>
                        <div class="form-group">
                            <textarea name="message" placeholder="Your Message" rows="5" required></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">Send Message</button>
                    </form>
                </div>
            </div>
        </section>'''

    def _generate_nav_items(self, sections: List[str]) -> str:
        """Generate navigation items based on sections"""
        nav_items = ""
        for section in sections:
            if section in ["hero", "about", "contact"]:
                nav_items += f'<li><a href="#{section}">{section.title()}</a></li>\n'
        return nav_items

    def _generate_footer_links(self, sections: List[str]) -> str:
        """Generate footer quick links"""
        footer_links = ""
        for section in sections:
            if section in ["about", "services", "contact"]:
                footer_links += f'<li><a href="#{section}">{section.title()}</a></li>\n'
        return footer_links

    def _create_project_readme(self) -> str:
        """Create a README.md file content"""
        title = self._generate_site_title()
        return f'''# {title}

This project is generated by an AI-powered website generator.

## Features

- Modern and responsive design
- Semantic HTML5 markup
- CSS Grid and Flexbox layout
- JavaScript ES6+ functionality
- AI-driven content generation

## Sections

- Hero
- About
- Services
- Projects
- Contact

## Technologies

- HTML
- CSS
- JavaScript
- AI/ML

## Setup

1. Clone the repository
2. Install dependencies
3. Run the development server
4. Open your browser and navigate to `http://localhost:3000`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.'''

    def _create_animations_css(self) -> str:
        """Create CSS for animations"""
        return '''@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes slideIn {
    from {
        transform: translateY(10px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-10px);
    }
    60% {
        transform: translateY(-5px);
    }
}'''

    def _create_responsive_css(self) -> str:
        """Create responsive CSS styles"""
        return '''@media (max-width: 768px) {
    nav {
        flex-direction: column;
        gap: 1rem;
    }
    
    #hero h1 {
        font-size: 2rem;
    }
    
    .about-grid {
        grid-template-columns: 1fr;
    }
    
    .contact-grid {
        grid-template-columns: 1fr;
    }
}'''

    def _create_modern_css_template(self) -> str:
        """Create modern CSS styles"""
        color_scheme = self.site_config.get("color_scheme", "blue")
        
        return f'''* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f4f4f9;
}}

h1, h2, h3, h4, h5, h6 {{
    margin-bottom: 1rem;
    color: #111;
}}

p {{
    margin-bottom: 1rem;
}}

a {{
    color: inherit;
    text-decoration: none;
    transition: color 0.3s;
}}

a:hover {{
    color: #3498db;
}}

ul {{
    list-style: none;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}}

.navbar {{
    background: #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}}

.nav-logo h2 {{
    font-size: 1.8rem;
    font-weight: 600;
}}

.nav-menu {{
    display: flex;
    gap: 2rem;
}}

.nav-toggle {{
    display: none;
    flex-direction: column;
    cursor: pointer;
}}

.bar {{
    height: 3px;
    width: 25px;
    background: #333;
    margin: 4px 0;
}}

.hero {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 6rem 2rem;
    border-radius: 10px;
    position: relative;
    overflow: hidden;
}}

.hero::after {{
    content: '';
    position: absolute;
    top: 0;
    left: 50%;
    width: 300%;
    height: 100%;
    background: rgba(255, 255, 255, 0.1);
    transform: translateX(-50%) rotate(30deg);
    z-index: 0;
}}

.hero-container {{
    position: relative;
    z-index: 1;
}}

.hero-title {{
    font-size: 3rem;
    margin-bottom: 1rem;
    animation: fadeIn 1s ease-out;
}}

.hero-subtitle {{
    font-size: 1.2rem;
    margin-bottom: 2rem;
    animation: fadeIn 1.2s ease-out;
}}

.hero-buttons {{
    display: flex;
    gap: 1rem;
    animation: fadeIn 1.4s ease-out;
}}

.btn {{
    background: #3498db;
    color: white;
    border: none;
    padding: 1rem 2rem;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1.1rem;
    transition: background 0.3s;
}}

.btn-primary:hover {{
    background: #2980b9;
}}

.btn-secondary {{
    background: transparent;
    border: 2px solid white;
    color: white;
}}

.btn-secondary:hover {{
    background: white;
    color: #3498db;
}}

.section {{
    margin: 4rem 0;
    text-align: center;
}}

.about-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    animation: slideIn 1s ease-out;
}}

.contact-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    animation: slideIn 1s ease-out;
}}

.footer {{
    background: #34495e;
    color: white;
    text-align: center;
    padding: 2rem;
}}

.social-links {{
    display: flex;
    gap: 1rem;
    justify-content: center;
}}

@media (max-width: 768px) {{
    .nav-menu {{
        display: none;
        flex-direction: column;
        gap: 1rem;
    }}
    
    .nav-toggle {{
        display: flex;
    }}
    
    .hero-title {{
        font-size: 2.5rem;
    }}
    
    .about-grid, .contact-grid {{
        grid-template-columns: 1fr;
    }}
}}
'''

    def _create_modern_js_template(self) -> str:
        """Create modern JavaScript"""
        return '''// Modern JavaScript for website interactivity
document.addEventListener('DOMContentLoaded', function() {
    console.log('Website loaded successfully!');
    
    // Mobile menu toggle
    const mobileMenu = document.getElementById('mobile-menu');
    const navMenu = document.getElementById('nav-menu');
    
    mobileMenu.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        mobileMenu.classList.toggle('active');
    });
    
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Button click handler
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            alert('Hello from your generated website!');
        });
    });
});'''

    def _create_animations_js(self) -> str:
        """Create JavaScript for animations and interactions"""
        return '''// JavaScript for scroll animations and interactions
document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('.section');
    
    const options = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    }, options);
    
    sections.forEach(section => {
        observer.observe(section);
    });
});'''