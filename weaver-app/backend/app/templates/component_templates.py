# Component templates for website generation

PORTFOLIO_TEMPLATE = {
    "sections": ["hero", "about", "projects", "skills", "contact"],
    "hero": {
        "title": "Welcome to My Portfolio",
        "subtitle": "I'm a passionate developer creating amazing digital experiences",
        "cta": "View My Work"
    },
    "about": {
        "title": "About Me",
        "content": "I'm a skilled professional with expertise in modern web technologies."
    },
    "projects": {
        "title": "My Projects",
        "items": [
            {"title": "Project 1", "description": "Description of project 1"},
            {"title": "Project 2", "description": "Description of project 2"},
            {"title": "Project 3", "description": "Description of project 3"}
        ]
    },
    "skills": {
        "title": "Skills",
        "items": ["HTML/CSS", "JavaScript", "React", "Node.js", "Python"]
    },
    "contact": {
        "title": "Get In Touch",
        "content": "Let's work together on your next project."
    }
}

BUSINESS_TEMPLATE = {
    "sections": ["hero", "services", "about", "testimonials", "contact"],
    "hero": {
        "title": "Transform Your Business",
        "subtitle": "Professional solutions for modern challenges",
        "cta": "Learn More"
    },
    "services": {
        "title": "Our Services",
        "items": [
            {"title": "Service 1", "description": "Professional service description"},
            {"title": "Service 2", "description": "Professional service description"},
            {"title": "Service 3", "description": "Professional service description"}
        ]
    },
    "about": {
        "title": "About Our Company",
        "content": "We are a leading provider of innovative business solutions."
    },
    "testimonials": {
        "title": "What Our Clients Say",
        "items": [
            {"name": "Client 1", "text": "Excellent service and results"},
            {"name": "Client 2", "text": "Professional and reliable"},
            {"name": "Client 3", "text": "Highly recommended"}
        ]
    },
    "contact": {
        "title": "Contact Us",
        "content": "Ready to start your project? Get in touch today."
    }
}

LANDING_PAGE_TEMPLATE = {
    "sections": ["hero", "features", "about", "cta", "contact"],
    "hero": {
        "title": "Welcome to Our Platform",
        "subtitle": "The solution you've been looking for",
        "cta": "Get Started"
    },
    "features": {
        "title": "Features",
        "items": [
            {"title": "Feature 1", "description": "Amazing feature description"},
            {"title": "Feature 2", "description": "Amazing feature description"},
            {"title": "Feature 3", "description": "Amazing feature description"}
        ]
    },
    "about": {
        "title": "About",
        "content": "Learn more about what makes us unique."
    },
    "cta": {
        "title": "Ready to Get Started?",
        "subtitle": "Join thousands of satisfied customers",
        "button": "Sign Up Now"
    },
    "contact": {
        "title": "Contact",
        "content": "Have questions? We're here to help."
    }
}

def get_template(site_type: str) -> dict:
    """Get the appropriate template based on site type"""
    templates = {
        "portfolio": PORTFOLIO_TEMPLATE,
        "business": BUSINESS_TEMPLATE,
        "landing_page": LANDING_PAGE_TEMPLATE
    }
    return templates.get(site_type, LANDING_PAGE_TEMPLATE)