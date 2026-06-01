import logging
import random

logger = logging.getLogger("glowup.chatbot")

class ProductRecommender:
    def recommend(self, skin_type: str, concerns: list) -> str:
        """
        Mock LLM product recommendation logic based on skin context.
        """
        logger.info(f"Generating recommendations for {skin_type} skin with concerns: {concerns}")
        
        products = []
        
        # Skin type logic
        if skin_type.lower() == "oily":
            products.append("CeraVe Renewing SA Cleanser")
            products.append("Paula's Choice 2% BHA Liquid Exfoliant")
        elif skin_type.lower() == "dry":
            products.append("La Roche-Posay Toleriane Hydrating Gentle Cleanser")
            products.append("The Ordinary Hyaluronic Acid 2% + B5")
        elif skin_type.lower() == "combination":
            products.append("COSRX Low pH Good Morning Gel Cleanser")
            products.append("Neutrogena Hydro Boost Water Gel")
        else:
            products.append("Cetaphil Daily Facial Cleanser")

        # Concerns logic
        if "Acne" in concerns:
            products.append("PanOxyl Acne Foaming Wash (10% Benzoyl Peroxide)")
            products.append("The Ordinary Niacinamide 10% + Zinc 1%")
        if "Redness" in concerns:
            products.append("Dr. Jart+ Cicapair Tiger Grass Color Correcting Treatment")
            
        # Select 2-3 random appropriate products
        selected = random.sample(products, min(3, len(products)))
        
        response_text = f"Based on your {skin_type} skin and concerns ({', '.join(concerns)}), I highly recommend checking out: "
        response_text += ", ".join(selected[:-1]) + (f", and {selected[-1]}." if len(selected) > 1 else f"{selected[0]}.")
        
        return response_text
