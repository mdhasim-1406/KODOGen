# KODOGEN AI Quality Assurance - Golden Prompt Test Suite
# Created by Kai (The Sentinel of Stability)

import json
import asyncio
import logging
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class GoldenPrompt:
    def __init__(self, id: str, category: str, prompt: str, expected_elements: List[str], 
                 complexity: str, validation_criteria: List[str]):
        self.id = id
        self.category = category
        self.prompt = prompt
        self.expected_elements = expected_elements
        self.complexity = complexity
        self.validation_criteria = validation_criteria
        self.test_results = {}

class AIQualityValidator:
    """
    AI Quality Validation System - Ensures AI generates production-ready code
    """
    
    def __init__(self):
        self.golden_prompts = self._initialize_golden_prompts()
        self.validation_results = {}
    
    def _initialize_golden_prompts(self) -> List[GoldenPrompt]:
        """Initialize the Golden Prompt test suite"""
        return [
            GoldenPrompt(
                id="GP001",
                category="Portfolio",
                prompt="Create a minimalist portfolio website for a UX designer named Sarah Chen who specializes in mobile app design and has 5 years of experience. Include a hero section, about page, projects showcase, and contact form. Use a clean, modern design with blue and white colors.",
                expected_elements=["navigation", "hero", "about", "projects", "contact", "responsive_design"],
                complexity="medium",
                validation_criteria=["semantic_html", "accessibility", "modern_css", "responsive_design", "clean_code"]
            ),
            
            GoldenPrompt(
                id="GP002", 
                category="Business",
                prompt="Build a professional website for a dental clinic called 'Bright Smiles Dentistry' that needs appointment booking, service information, team profiles, and patient testimonials. Use a trustworthy, medical-professional design with blue and green colors.",
                expected_elements=["header", "services", "team", "testimonials", "booking", "contact"],
                complexity="high",
                validation_criteria=["form_functionality", "professional_design", "call_to_action", "trust_elements"]
            ),
            
            GoldenPrompt(
                id="GP003",
                category="Creative",
                prompt="Design a vibrant landing page for a music festival called 'SoundWave 2025' featuring lineup information, ticket purchasing, venue details, and social media integration. Use bold, energetic colors and modern festival aesthetics.",
                expected_elements=["hero_banner", "lineup", "tickets", "venue", "social_media"],
                complexity="high",
                validation_criteria=["visual_impact", "event_information", "CTA_buttons", "mobile_optimization"]
            ),
            
            GoldenPrompt(
                id="GP004",
                category="E-commerce",
                prompt="Create an online store for handmade jewelry called 'Artisan Gems' with product galleries, shopping cart functionality, customer reviews, and secure checkout process. Use elegant, luxury design with gold and black colors.",
                expected_elements=["product_grid", "product_details", "cart", "reviews", "checkout"],
                complexity="very_high",
                validation_criteria=["ecommerce_flow", "product_display", "user_experience", "form_validation"]
            ),
            
            GoldenPrompt(
                id="GP005",
                category="Blog",
                prompt="Build a tech blog website called 'CodeCraft' for sharing programming tutorials and industry insights. Include article listings, categories, search functionality, author profiles, and comment sections. Use a clean, developer-friendly design.",
                expected_elements=["article_list", "categories", "search", "author_bio", "comments"],
                complexity="medium",
                validation_criteria=["content_structure", "readability", "navigation", "search_functionality"]
            ),
            
            GoldenPrompt(
                id="GP006",
                category="Restaurant",
                prompt="Create a restaurant website for 'Bella Vista Italian' featuring an online menu with prices, reservation system, photo gallery of dishes, chef information, and location details. Use warm, inviting colors and Italian-inspired design.",
                expected_elements=["menu", "reservations", "gallery", "chef", "location", "contact"],
                complexity="medium",
                validation_criteria=["menu_display", "reservation_form", "image_gallery", "local_business_info"]
            ),
            
            GoldenPrompt(
                id="GP007",
                category="Startup",
                prompt="Design a SaaS landing page for 'DataFlow Analytics' - a business intelligence tool. Include feature highlights, pricing tiers, customer testimonials, free trial signup, and integration showcases. Use professional blue and white design with modern gradients.",
                expected_elements=["hero", "features", "pricing", "testimonials", "trial_signup", "integrations"],
                complexity="high",
                validation_criteria=["conversion_optimization", "pricing_clarity", "feature_presentation", "trust_signals"]
            ),
            
            GoldenPrompt(
                id="GP008",
                category="Non-Profit",
                prompt="Build a website for 'Ocean Clean Initiative' environmental organization. Include mission statement, current projects, donation functionality, volunteer signup, impact statistics, and news updates. Use ocean-inspired blue and green colors.",
                expected_elements=["mission", "projects", "donations", "volunteer", "impact_stats", "news"],
                complexity="medium",
                validation_criteria=["emotional_connection", "donation_flow", "volunteer_engagement", "impact_presentation"]
            )
        ]
    
    async def run_golden_prompt_validation(self, ai_generator_class) -> Dict[str, Any]:
        """
        Run the complete Golden Prompt validation suite
        """
        logger.info("🧪 Starting Golden Prompt AI validation suite...")
        
        validation_results = {
            "start_time": datetime.now().isoformat(),
            "total_prompts": len(self.golden_prompts),
            "passed": 0,
            "failed": 0,
            "results": {}
        }
        
        for prompt in self.golden_prompts:
            try:
                logger.info(f"🎯 Testing {prompt.id}: {prompt.category}")
                
                # Generate website with AI
                result = await self._test_single_prompt(prompt, ai_generator_class)
                validation_results["results"][prompt.id] = result
                
                if result["overall_score"] >= 75:  # 75% threshold for passing
                    validation_results["passed"] += 1
                    logger.info(f"✅ {prompt.id} PASSED with {result['overall_score']}% score")
                else:
                    validation_results["failed"] += 1
                    logger.warning(f"❌ {prompt.id} FAILED with {result['overall_score']}% score")
                    
            except Exception as e:
                logger.error(f"💥 {prompt.id} ERROR: {str(e)}")
                validation_results["results"][prompt.id] = {
                    "error": str(e),
                    "overall_score": 0
                }
                validation_results["failed"] += 1
        
        validation_results["end_time"] = datetime.now().isoformat()
        validation_results["pass_rate"] = (validation_results["passed"] / validation_results["total_prompts"]) * 100
        
        logger.info(f"🏁 Golden Prompt validation complete: {validation_results['pass_rate']}% pass rate")
        
        return validation_results
    
    async def _test_single_prompt(self, prompt: GoldenPrompt, ai_generator_class) -> Dict[str, Any]:
        """Test a single Golden Prompt"""
        import uuid
        task_id = str(uuid.uuid4())
        
        # Initialize AI generator
        ai_generator = ai_generator_class(task_id=task_id, prompt=prompt.prompt)
        
        # Generate website
        await ai_generator.generate_website_with_ai()
        
        # Validate the generated code
        generated_files = await self._extract_generated_files(ai_generator.project_dir)
        
        # Run validation checks
        validation_result = {
            "prompt_id": prompt.id,
            "category": prompt.category,
            "complexity": prompt.complexity,
            "html_quality": self._validate_html_quality(generated_files.get("html", "")),
            "css_quality": self._validate_css_quality(generated_files.get("css", "")),
            "js_quality": self._validate_javascript_quality(generated_files.get("javascript", "")),
            "accessibility": self._validate_accessibility(generated_files.get("html", "")),
            "responsiveness": self._validate_responsiveness(generated_files.get("css", "")),
            "expected_elements": self._validate_expected_elements(generated_files, prompt.expected_elements),
            "overall_score": 0
        }
        
        # Calculate overall score
        scores = [
            validation_result["html_quality"]["score"],
            validation_result["css_quality"]["score"],
            validation_result["accessibility"]["score"],
            validation_result["responsiveness"]["score"],
            validation_result["expected_elements"]["score"]
        ]
        
        validation_result["overall_score"] = sum(scores) / len(scores)
        
        return validation_result
    
    async def _extract_generated_files(self, project_dir: str) -> Dict[str, str]:
        """Extract generated files from project directory"""
        import os
        
        files = {}
        
        # Read HTML
        html_path = os.path.join(project_dir, "index.html")
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                files["html"] = f.read()
        
        # Read CSS
        css_path = os.path.join(project_dir, "css", "styles.css")
        if os.path.exists(css_path):
            with open(css_path, 'r', encoding='utf-8') as f:
                files["css"] = f.read()
        
        # Read JavaScript
        js_path = os.path.join(project_dir, "js", "script.js")
        if os.path.exists(js_path):
            with open(js_path, 'r', encoding='utf-8') as f:
                files["javascript"] = f.read()
        
        return files
    
    def _validate_html_quality(self, html_content: str) -> Dict[str, Any]:
        """Validate HTML structure and quality"""
        score = 0
        issues = []
        
        checks = [
            ("DOCTYPE declaration", "<!DOCTYPE html>" in html_content, 15),
            ("Language attribute", 'lang="' in html_content, 10),
            ("Meta viewport", "viewport" in html_content, 15),
            ("Semantic HTML5", any(tag in html_content for tag in ["<header>", "<main>", "<section>", "<article>", "<footer>"]), 20),
            ("Valid structure", "<html>" in html_content and "</html>" in html_content, 10),
            ("Head section", "<head>" in html_content and "</head>" in html_content, 10),
            ("Body section", "<body>" in html_content and "</body>" in html_content, 10),
            ("Title tag", "<title>" in html_content, 10)
        ]
        
        for check_name, condition, points in checks:
            if condition:
                score += points
            else:
                issues.append(f"Missing: {check_name}")
        
        return {
            "score": min(score, 100),
            "issues": issues,
            "max_score": 100
        }
    
    def _validate_css_quality(self, css_content: str) -> Dict[str, Any]:
        """Validate CSS quality and modern practices"""
        score = 0
        issues = []
        
        checks = [
            ("CSS Grid usage", "grid" in css_content, 20),
            ("Flexbox usage", "flex" in css_content, 20),
            ("Custom properties", "--" in css_content, 15),
            ("Media queries", "@media" in css_content, 25),
            ("Modern units", any(unit in css_content for unit in ["rem", "em", "vh", "vw"]), 10),
            ("Transitions/animations", any(prop in css_content for prop in ["transition", "animation", "transform"]), 10)
        ]
        
        for check_name, condition, points in checks:
            if condition:
                score += points
            else:
                issues.append(f"Missing: {check_name}")
        
        return {
            "score": min(score, 100),
            "issues": issues,
            "max_score": 100
        }
    
    def _validate_accessibility(self, html_content: str) -> Dict[str, Any]:
        """Validate accessibility features"""
        score = 0
        issues = []
        
        checks = [
            ("Alt attributes", 'alt="' in html_content, 25),
            ("ARIA labels", 'aria-label' in html_content, 20),
            ("Heading hierarchy", "<h1>" in html_content, 15),
            ("Skip links", 'href="#' in html_content, 10),
            ("Form labels", "<label>" in html_content, 15),
            ("Focus management", 'tabindex' in html_content, 15)
        ]
        
        for check_name, condition, points in checks:
            if condition:
                score += points
            else:
                issues.append(f"Missing: {check_name}")
        
        return {
            "score": min(score, 100),
            "issues": issues,
            "max_score": 100
        }
    
    def _validate_responsiveness(self, css_content: str) -> Dict[str, Any]:
        """Validate responsive design implementation"""
        score = 0
        issues = []
        
        # Count media queries
        media_query_count = css_content.count("@media")
        
        checks = [
            ("Mobile breakpoint", "max-width: 768px" in css_content or "max-width: 767px" in css_content, 30),
            ("Tablet breakpoint", "max-width: 1024px" in css_content or "max-width: 1023px" in css_content, 25),
            ("Multiple breakpoints", media_query_count >= 2, 25),
            ("Flexible layouts", "flex" in css_content or "grid" in css_content, 20)
        ]
        
        for check_name, condition, points in checks:
            if condition:
                score += points
            else:
                issues.append(f"Missing: {check_name}")
        
        return {
            "score": min(score, 100),
            "issues": issues,
            "max_score": 100
        }
    
    def _validate_expected_elements(self, files: Dict[str, str], expected_elements: List[str]) -> Dict[str, Any]:
        """Validate that expected elements are present"""
        html_content = files.get("html", "").lower()
        found_elements = []
        missing_elements = []
        
        element_mappings = {
            "navigation": ["<nav>", "navbar", "navigation"],
            "hero": ["hero", "banner", "jumbotron"],
            "about": ["about", "about-us"],
            "projects": ["project", "portfolio", "work"],
            "contact": ["contact", "contact-us"],
            "services": ["service", "offering"],
            "testimonials": ["testimonial", "review"],
            "gallery": ["gallery", "image"],
            "menu": ["menu", "food"],
            "booking": ["book", "reservation", "appointment"]
        }
        
        for element in expected_elements:
            element_found = False
            if element in element_mappings:
                for pattern in element_mappings[element]:
                    if pattern in html_content:
                        element_found = True
                        break
            else:
                element_found = element.lower() in html_content
            
            if element_found:
                found_elements.append(element)
            else:
                missing_elements.append(element)
        
        score = (len(found_elements) / len(expected_elements)) * 100 if expected_elements else 100
        
        return {
            "score": score,
            "found_elements": found_elements,
            "missing_elements": missing_elements,
            "total_expected": len(expected_elements)
        }

# Global validator instance
ai_quality_validator = AIQualityValidator()