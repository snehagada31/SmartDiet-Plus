# recipes_list.py

recipes_data = [
    {
        'id': 1,
        'title': 'Vegetarian Pasta Primavera',
        'image': '/static/images/vegetarian_pasta.png',
        'diet': ['vegetarian'],
        'allergies': ['gluten'],
        'activity_level_suitability': ['medium'],
        'ingredients': [
            '200g whole wheat pasta',
            '1 cup broccoli florets',
            '1/2 cup sliced carrots',
            '1/2 cup chopped bell peppers (any color)',
            '1/4 cup cherry tomatoes, halved',
            '2 cloves garlic, minced',
            '2 tbsp olive oil',
            'Salt and pepper to taste',
            'Fresh basil for garnish'
        ],
        'instructions': [
            'Cook pasta according to package directions.',
            'In a large skillet, heat olive oil over medium heat. Add garlic, broccoli, carrots, and bell peppers. Sauté for 5-7 minutes until tender-crisp.',
            'Add cherry tomatoes and cooked pasta to the skillet. Toss to combine.',
            'Season with salt and pepper. Garnish with fresh basil and serve.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=pasta_primavera_link'
    },
    {
        'id': 2,
        'title': 'Roasted Chicken with Herbs',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiYtdHZsyI1t3X850mZJZ27_ja_HnodkYT8w&s',
        'diet': ['non-vegetarian'],
        'allergies': [],
        'activity_level_suitability': ['high'],
        'ingredients': [
            '4 chicken thighs (bone-in, skin-on)',
            '2 tbsp olive oil',
            '1 tbsp dried rosemary',
            '1 tbsp dried thyme',
            '1 tsp garlic powder',
            'Salt and black pepper to taste',
            '1 lemon, sliced (optional)'
        ],
        'instructions': [
            'Preheat oven to 200°C (400°F).',
            'Pat chicken thighs dry with paper towels.',
            'In a small bowl, combine olive oil, rosemary, thyme, garlic powder, salt, and pepper.',
            'Rub the herb mixture all over the chicken thighs.',
            'Place chicken in a baking dish, optionally with lemon slices.',
            'Roast for 35-45 minutes, or until internal temperature reaches 75°C (165°F) and skin is crispy.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=roasted_chicken_link'
    },
    {
        'id': 3,
        'title': 'Vegan Lentil Soup',
        'image': 'https://www.eatingwell.com/thmb/AZdGSagOj8VtZPnpcVdD8ttRk3k=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/vegan-lentil-stew-0b016185b40446ba98409c75dfeaef7f.jpg',
        'diet': ['vegan', 'vegetarian'],
        'allergies': [],
        'activity_level_suitability': ['low', 'medium'],
        'ingredients': [
            '1 cup brown or green lentils, rinsed',
            '6 cups vegetable broth',
            '1 large onion, chopped',
            '2 carrots, diced',
            '2 celery stalks, diced',
            '2 cloves garlic, minced',
            '1 (14.5 oz) can diced tomatoes, undrained',
            '1 tsp dried thyme',
            '1 tsp ground cumin',
            'Salt and pepper to taste',
            '2 tbsp olive oil'
        ],
        'instructions': [
            'Heat olive oil in a large pot over medium heat. Add onion, carrots, and celery. Sauté for 5-7 minutes until softened.',
            'Add garlic, thyme, and cumin. Cook for 1 minute more until fragrant.',
            'Stir in lentils, vegetable broth, and diced tomatoes. Bring to a boil, then reduce heat, cover, and simmer for 25-30 minutes, or until lentils are tender.',
            'Season with salt and pepper. Serve hot.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=vegan_lentil_soup_link'
    },
    {
        'id': 4,
        'title': 'Gluten-Free Berry Smoothie Bowl',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOmVj-W8WCAWTM_zMAiGClw-uRejIrCgjLCA&s',
        'diet': ['vegan', 'vegetarian', 'gluten-free'],
        'allergies': ['dairy'],
        'activity_level_suitability': ['low'],
        'ingredients': [
            '1 cup mixed berries (frozen)',
            '1 ripe banana (frozen or fresh)',
            '1/2 cup unsweetened almond milk (or other plant-based milk)',
            '1 tbsp chia seeds',
            'Optional toppings: fresh berries, granola (gluten-free), shredded coconut, nuts'
        ],
        'instructions': [
            'Combine frozen berries, banana, almond milk, and chia seeds in a blender.',
            'Blend until completely smooth and thick. Add more milk if needed to reach desired consistency.',
            'Pour into a bowl and arrange your favorite toppings.',
            'Serve immediately.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=gf_smoothie_bowl_link'
    },
    {
        'id': 5,
        'title': 'Spicy Shrimp Tacos',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR14L718aig02XGJa-WCMK4pcisWgL4y81zjw&s',
        'diet': ['non-vegetarian'],
        'allergies': ['shellfish', 'corn'],
        'activity_level_suitability': ['medium', 'high'],
        'ingredients': [
            '500g raw shrimp, peeled and deveined',
            '1 tbsp olive oil',
            '1 tsp chili powder',
            '1/2 tsp cumin',
            '1/4 tsp cayenne pepper (adjust to taste)',
            'Salt and pepper to taste',
            '8 small corn or flour tortillas',
            'Toppings: shredded cabbage, diced avocado, lime wedges, cilantro'
        ],
        'instructions': [
            'In a bowl, toss shrimp with olive oil, chili powder, cumin, cayenne, salt, and pepper.',
            'Heat a large skillet over medium-high heat. Add shrimp and cook for 2-3 minutes per side, until pink and opaque.',
            'Warm tortillas according to package directions.',
            'Assemble tacos with shrimp and desired toppings. Serve with lime wedges.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=spicy_shrimp_tacos_link'
    },
    {
        'id': 6,
        'title': 'Classic Margherita Pizza',
        'image': '/static/images/margherita_pizza.png',
        'diet': ['vegetarian'],
        'allergies': ['gluten', 'dairy'],
        'activity_level_suitability': ['medium'],
        'ingredients': [
            '1 pizza dough (store-bought or homemade)',
            '1/2 cup tomato sauce',
            '1 cup fresh mozzarella cheese, sliced or torn',
            'Fresh basil leaves',
            '1 tbsp olive oil',
            'Salt to taste'
        ],
        'instructions': [
            'Preheat oven to 220°C (425°F) with a pizza stone or baking sheet inside.',
            'Stretch or roll out pizza dough on a lightly floured surface.',
            'Spread tomato sauce evenly over the dough, leaving a crust.',
            'Arrange mozzarella slices over the sauce.',
            'Carefully transfer pizza to the hot oven.',
            'Bake for 10-15 minutes, or until crust is golden and cheese is bubbly and lightly browned.',
            'Remove from oven, scatter fresh basil leaves, drizzle with olive oil, and sprinkle with salt. Slice and serve hot.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=margherita_pizza_link'
    },
    {
        'id': 7,
        'title': 'Chicken and Vegetable Skewers',
        'image': '/static/images/chicken_skewers.png',
        'diet': ['non-vegetarian'],
        'allergies': [],
        'activity_level_suitability': ['high'],
        'ingredients': [
            '500g boneless, skinless chicken breast, cut into 1-inch cubes',
            '1 bell pepper (any color), cut into 1-inch pieces',
            '1 zucchini, cut into 1/2-inch thick half-moons',
            '1 red onion, cut into wedges',
            '2 tbsp olive oil',
            '1 tbsp dried oregano',
            '1 tsp paprika',
            'Salt and pepper to taste',
            'Wooden or metal skewers'
        ],
        'instructions': [
            'If using wooden skewers, soak them in water for 30 minutes to prevent burning.',
            'In a large bowl, combine chicken, bell pepper, zucchini, and red onion.',
            'Drizzle with olive oil, then sprinkle with oregano, paprika, salt, and pepper. Toss to coat evenly.',
            'Thread chicken and vegetables alternately onto skewers.',
            'Grill or broil for 10-15 minutes, turning occasionally, until chicken is cooked through and vegetables are tender-crisp.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=chicken_skewers_link'
    },
    {
        'id': 8,
        'title': 'Vegetarian Chili',
        'image': '/static/images/vegetarian_chili.png',
        'diet': ['vegetarian', 'vegan'],
        'allergies': [],
        'activity_level_suitability': ['medium', 'high'],
        'ingredients': [
            '1 tbsp olive oil',
            '1 large onion, chopped',
            '2 cloves garlic, minced',
            '1 bell pepper, chopped',
            '1 (14.5 oz) can diced tomatoes, undrained',
            '1 (15 oz) can kidney beans, rinsed and drained',
            '1 (15 oz) can black beans, rinsed and drained',
            '1 cup vegetable broth',
            '2 tbsp chili powder',
            '1 tbsp cumin',
            '1/2 tsp smoked paprika',
            'Salt and pepper to taste',
            'Optional: avocado, sour cream (or vegan alternative), shredded cheese for topping'
        ],
        'instructions': [
            'Heat olive oil in a large pot over medium heat. Add onion and bell pepper; cook until softened, about 5-7 minutes.',
            'Add garlic, chili powder, cumin, and smoked paprika. Cook for 1 minute until fragrant.',
            'Stir in diced tomatoes, kidney beans, black beans, and vegetable broth. Bring to a simmer.',
            'Reduce heat, cover, and let simmer for at least 20 minutes (longer for more flavor).',
            'Season with salt and pepper. Serve hot with desired toppings.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=vegetarian_chili_link'
    },
    {
        'id': 9,
        'title': 'Oatmeal with Berries and Nuts',
        'image': '/static/images/oatmeal_berries.png',
        'diet': ['vegetarian', 'vegan', 'gluten-free'],
        'allergies': ['nuts'],
        'activity_level_suitability': ['low'],
        'ingredients': [
            '1/2 cup rolled oats (gluten-free if needed)',
            '1 cup water or plant-based milk',
            '1/2 cup mixed berries (fresh or frozen)',
            '1 tbsp chopped nuts (almonds, walnuts, pecans)',
            '1 tsp maple syrup or honey (optional)'
        ],
        'instructions': [
            'Combine oats and water/milk in a small saucepan. Bring to a simmer over medium heat.',
            'Cook for 5-7 minutes, stirring occasionally, until liquid is absorbed and oats are creamy.',
            'Stir in berries. Transfer to a bowl.',
            'Top with chopped nuts and a drizzle of maple syrup/honey if desired. Serve warm.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=oatmeal_berries_link'
    },
    {
        'id': 10,
        'title': 'Baked Salmon with Asparagus',
        'image': '/static/images/baked_salmon.png',
        'diet': ['non-vegetarian', 'gluten-free'],
        'allergies': ['fish'],
        'activity_level_suitability': ['medium', 'high'],
        'ingredients': [
            '2 salmon fillets',
            '1 bunch asparagus, trimmed',
            '1 tbsp olive oil',
            '1/2 lemon, sliced',
            'Salt and black pepper to taste',
            '1 tsp dried dill (optional)'
        ],
        'instructions': [
            'Preheat oven to 200°C (400°F). Line a baking sheet with parchment paper.',
            'Place salmon fillets and asparagus on the baking sheet.',
            'Drizzle with olive oil, season with salt, pepper, and dill.',
            'Top salmon with lemon slices.',
            'Bake for 12-15 minutes, or until salmon is cooked through and flakes easily with a fork, and asparagus is tender-crisp.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=baked_salmon_link'
    },
    {
        'id': 11,
        'title': 'Mediterranean Quinoa Salad',
        'image':"https://cdn.loveandlemons.com/wp-content/uploads/2020/08/quinoa-salad.jpg",
        'diet': ['vegetarian', 'vegan', 'gluten-free'],
        'allergies': [],
        'activity_level_suitability': ['low', 'medium'],
        'ingredients': [
            '1 cup cooked quinoa',
            '1/2 cup chopped cucumber',
            '1/2 cup halved cherry tomatoes',
            '1/4 cup chopped red onion',
            '1/4 cup crumbled feta cheese (omit for vegan)',
            '2 tbsp chopped fresh parsley',
            '2 tbsp olive oil',
            '1 tbsp lemon juice',
            'Salt and pepper to taste'
        ],
        'instructions': [
            'In a large bowl, combine cooked quinoa, cucumber, cherry tomatoes, red onion, feta (if using), and parsley.',
            'In a small bowl, whisk together olive oil, lemon juice, salt, and pepper.',
            'Pour dressing over the salad and toss gently to combine.',
            'Serve chilled or at room temperature.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=quinoa_salad_link'
    },
    {
        'id': 12,
        'title': 'Spinach and Mushroom Omelette',
        'image': 'https://www.thechunkychef.com/wp-content/uploads/2017/11/Cheesy-Mushroom-Omelet.jpg',
        'diet': ['vegetarian'],
        'allergies': ['dairy'],
        'activity_level_suitability': ['low', 'medium'],
        'ingredients': [
            '3 large eggs',
            '1/4 cup milk or water',
            '1 tbsp olive oil',
            '1 cup fresh spinach',
            '1/2 cup sliced mushrooms',
            'Salt and pepper to taste',
            '2 tbsp shredded cheese (cheddar or mozzarella, optional)'
        ],
        'instructions': [
            'In a bowl, whisk eggs with milk/water, salt, and pepper until well combined.',
            'Heat olive oil in a non-stick skillet over medium heat. Add mushrooms and cook until softened, about 3-5 minutes.',
            'Add spinach and cook until wilted, about 1-2 minutes.',
            'Pour egg mixture over the vegetables in the skillet. Cook without stirring until edges begin to set.',
            'Sprinkle with cheese if using. Cook until eggs are mostly set but still slightly moist on top.',
            'Fold omelette in half and slide onto a plate. Serve immediately.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=omelette_link'
    },
    # --- Newly Added Recipes with details and activity_level_suitability ---
    # Low Activity Meals
    {
        'id': 13,
        'title': 'Oatmeal with fruits',
        'image': 'https://cdn.aboutamom.com/uploads/2017/01/Oatmeal2.png',
        'diet': ['vegetarian', 'vegan', 'gluten-free'],
        'allergies': [],
        'activity_level_suitability': ['low'],
        'ingredients': [
            '1/2 cup rolled oats', '1 cup water or milk (dairy or plant-based)',
            '1/2 cup mixed fruits (berries, banana slices)', '1 tbsp honey or maple syrup (optional)',
            'Pinch of cinnamon (optional)'
        ],
        'instructions': [
            'Combine oats and water/milk in a saucepan. Bring to a simmer over medium heat.',
            'Cook for 5-7 minutes, stirring occasionally, until liquid is absorbed and oats are creamy.',
            'Stir in fruits. Sweeten with honey/maple syrup if desired. Serve warm.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=oatmeal_fruits_link'
    },
    {
        'id': 14,
        'title': 'Boiled eggs with toast',
        'image': 'https://media.self.com/photos/5a299f4b83ab3f54feacf511/1:1/w_773,h_773,c_limit/0517-hard-boiled-egg-toast.jpg',
        'diet': ['non-vegetarian'],
        'allergies': ['gluten'],
        'activity_level_suitability': ['low'],
        'ingredients': [
            '2 large eggs', '2 slices whole wheat toast', 'Salt and pepper to taste',
            'Butter or avocado for toast (optional)'
        ],
        'instructions': [
            'Place eggs in a saucepan and cover with cold water. Bring to a rolling boil, then remove from heat, cover, and let stand for 8-10 minutes for hard-boiled eggs.',
            'Drain and cool eggs under cold water. Peel and halve.',
            'Toast bread. Serve boiled eggs with toast, seasoned with salt and pepper.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=poha_link'
    },
    {
        'id': 15,
        'title': 'Poha',
        'image': 'https://thegaruskitchen.com/wp-content/uploads/2025/02/Jain-Poha-Recipe.jpeg',
        'diet': ['vegetarian'],
        'allergies': ['peanuts'],
        'activity_level_suitability': ['low'],
        'ingredients': [
            '1 cup thick flattened rice (poha)', '1/4 cup chopped onion', '1/4 cup chopped potato',
            '1/4 cup green peas', '1-2 green chilies, slit', '1 tsp mustard seeds', '1/2 tsp turmeric powder',
            '1 tbsp oil', 'Salt to taste', 'Lemon wedges and fresh coriander for garnish',
            '1/4 cup roasted peanuts (optional)'
        ],
        'instructions': [
            'Rinse poha gently in a sieve until soft, drain and set aside.',
            'Heat oil in a pan, add mustard seeds. Once they splutter, add curry leaves, green chilies, and onion. Sauté until onion is translucent.',
            'Add potato and peas, cook until tender. Add turmeric powder and salt.',
            'Add the rinsed poha and mix well. Cover and cook for 2-3 minutes on low heat.',
            'Garnish with roasted peanuts, fresh coriander, and a squeeze of lemon juice. Serve hot.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=fruit_salad_link'
    },
    {
        'id': 16,
        'title': 'Fruit salad',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXgdqwalEV0wkfilPZnKQoCq4OFaI3Tj5dRQ&s',
        'diet': ['vegetarian', 'vegan', 'gluten-free'],
        'allergies': [],
        'activity_level_suitability': ['low'],
        'ingredients': [
            '1 cup chopped melon (cantaloupe, honeydew)', '1 cup chopped apples', '1 cup grapes (halved)',
            '1/2 cup berries (strawberries, blueberries)', '1 banana, sliced', '1 tbsp honey or maple syrup (optional)',
            'Juice of 1/2 lime'
        ],
        'instructions': [
            'Wash and chop all fruits. Combine them in a large bowl.',
            'Drizzle with honey or maple syrup (if using) and lime juice. Toss gently to combine.',
            'Serve chilled.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=grilled_paneer_salad_link'
    },
    {
        'id': 17,
        'title': 'Grilled paneer salad',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxp710NOORBH4zdi85Aizy_sx9ZsLvJ4wg_Q&s',
        'diet': ['vegetarian'],
        'allergies': ['dairy'],
        'activity_level_suitability': ['low', 'medium'],
        'ingredients': [
            '200g paneer, cubed', '1 cup mixed greens', '1/2 cup cherry tomatoes, halved',
            '1/4 cup sliced cucumber', '1/4 cup sliced bell peppers', '2 tbsp olive oil',
            '1 tbsp lemon juice', '1 tsp dried oregano', 'Salt and pepper to taste'
        ],
        'instructions': [
            'Toss paneer cubes with 1 tbsp olive oil, oregano, salt, and pepper. Grill or pan-fry until golden brown on all sides.',
            'In a large bowl, combine mixed greens, cherry tomatoes, cucumber, and bell peppers.',
            'Whisk together remaining olive oil, lemon juice, salt, and pepper to make a dressing.',
            'Add grilled paneer to the salad. Pour dressing over the salad and toss gently. Serve immediately.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=veg_soup_bread_link'
    },
    {
        'id': 18,
        'title': 'Vegetable soup with bread',
        'image': 'https://theshaziablog.com/wp-content/uploads/2021/12/DSC00301-2-500x500.jpg',
        'diet': ['vegetarian', 'vegan'],
        'allergies': ['gluten'],
        'activity_level_suitability': ['low'],
        'ingredients': [
            '1 tbsp olive oil', '1 onion, chopped', '2 carrots, diced', '2 celery stalks, diced',
            '4 cups vegetable broth', '1 cup mixed vegetables (peas, corn, green beans)',
            'Salt and pepper to taste', '2 slices whole wheat bread (for serving)'
        ],
        'instructions': [
            'Heat olive oil in a pot. Sauté onion, carrots, and celery until softened.',
            'Add vegetable broth and bring to a simmer. Add mixed vegetables and cook until tender.',
            'Season with salt and pepper. Serve hot with a side of bread.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=mixed_veg_curry_roti_link'
    },
    {
        'id': 19,
        'title': 'Mixed veg curry with roti',
        'image': 'https://mykitchentrials.wordpress.com/wp-content/uploads/2011/08/img_1697.jpg',
        'diet': ['vegetarian'],
        'allergies': ['gluten'],
        'activity_level_suitability': ['low', 'medium'],
        'ingredients': [
            '1 cup mixed vegetables (cauliflower, potato, carrots, peas)', '1 onion, chopped',
            '1 tomato, chopped', '1 tbsp ginger-garlic paste', '1 tsp cumin powder',
            '1 tsp coriander powder', '1/2 tsp turmeric powder', '1/2 tsp red chili powder',
            '2 tbsp oil', 'Salt to taste', 'Water as needed', 'Whole wheat flour for roti'
        ],
        'instructions': [
            'Heat oil in a pan, sauté onion until golden. Add ginger-garlic paste, cook for 1 minute.',
            'Add chopped tomato and cook until soft. Add all dry spices and cook for 2 minutes.',
            'Add mixed vegetables and a little water. Cover and cook until vegetables are tender.',
            'Serve hot with freshly made rotis.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=khichdi_link'
    },
    {
        'id': 20,
        'title': 'Khichdi',
        'image': 'https://carveyourcraving.com/wp-content/uploads/2023/01/Daliya-khichdi.jpg',
        'diet': ['vegetarian', 'vegan', 'gluten-free'],
        'allergies': [],
        'activity_level_suitability': ['low'],
        'ingredients': [
            '1/2 cup rice', '1/4 cup split yellow lentils (moong dal)', '3 cups water',
            '1/4 tsp turmeric powder', 'Pinch of asafoetida (hing)', '1 tsp cumin seeds',
            '1 tbsp ghee or oil', 'Salt to taste'
        ],
        'instructions': [
            'Wash rice and dal thoroughly. Combine in a pressure cooker or pot with water, turmeric, and salt.',
            'Pressure cook for 2-3 whistles or cook in a pot until rice and dal are soft and mushy.',
            'In a small pan, heat ghee/oil. Add cumin seeds and asafoetida. Once spluttering, pour over the cooked khichdi.',
            'Mix well and serve hot, optionally with curd or pickle.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=veg_wrap_link'
    },
    {
        'id': 21,
        'title': 'Veg wrap',
        'image': 'https://www.acouplecooks.com/wp-content/uploads/2023/02/Veggie-Wrap-002.jpg',
        'diet': ['vegetarian'],
        'allergies': ['gluten'],
        'activity_level_suitability': ['low', 'medium'],
        'ingredients': [
            '1 large tortilla or chapati', '1/2 cup mixed chopped vegetables (cabbage, carrots, bell peppers)',
            '2 tbsp hummus or green chutney', 'Salt and pepper to taste', '1 tsp oil'
        ],
        'instructions': [
            'Heat oil in a pan, sauté chopped vegetables until tender-crisp. Season with salt and pepper.',
            'Warm the tortilla/chapati. Spread hummus or chutney evenly over it.',
            'Place the sautéed vegetables in the center. Roll up tightly.',
            'Serve immediately.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=quinoa_veggies_link'
    },
    {
        'id': 22,
        'title': 'Dalia khichdi',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTeVsuoOBYKATvuyDc2LImZ4zDl7zjCUnTkig&s',
        'diet': ['vegetarian', 'vegan'],
        'allergies': ['gluten'],
        'activity_level_suitability': ['low'],
        'ingredients': [
            '1/2 cup broken wheat (dalia)', '1/4 cup split green gram (moong dal)', '3 cups water',
            '1/2 cup mixed vegetables (carrots, peas, beans)', '1 onion, chopped', '1 tomato, chopped',
            '1 tsp ginger-garlic paste', '1 tsp cumin seeds', '1 tbsp oil', 'Salt to taste'
        ],
        'instructions': [
            'Wash dal and dalia. Heat oil in a pressure cooker. Add cumin seeds. When they splutter, add onion and sauté until golden.',
            'Add ginger-garlic paste and tomato, cook until soft. Add mixed vegetables, dalia, moong dal, water, and salt.',
            'Pressure cook for 3-4 whistles or until dalia is tender. Serve hot.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=dalia_khichdi_link'
    },
    {
        'id': 23,
        'title': 'Veg pulao',
        'image': 'https://www.cubesnjuliennes.com/wp-content/uploads/2019/11/Veg-Pulao-2.jpg',
        'diet': ['vegetarian', 'vegan'],
        'allergies': [],
        'activity_level_suitability': ['low', 'medium'],
        'ingredients': [
            '1 cup basmati rice, soaked', '2 cups mixed vegetables (peas, carrots, potatoes)',
            '1 onion, sliced', '1 tbsp ginger-garlic paste', '1 tsp whole spices (cardamom, cinnamon, cloves)',
            '1 tsp cumin seeds', '2 tbsp oil', 'Salt to taste', '2 cups water'
        ],
        'instructions': [
            'Heat oil in a pot. Add whole spices and cumin seeds. Sauté for a few seconds.',
            'Add sliced onion and sauté until golden. Add ginger-garlic paste and cook for 1 minute.',
            'Add mixed vegetables and cook for 5 minutes. Add soaked rice, salt, and water.',
            'Bring to a boil, then reduce heat, cover, and cook until water is absorbed and rice is tender. Serve hot.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=veg_pulao_link'
    },

    # Medium Activity Meals
    {
        'id': 24,
        'title': 'Idli with chutney',
        'image': 'https://www.sailusfood.com/wp-content/uploads/2018/06/kara-chutney.jpg',
        'diet': ['vegetarian', 'vegan'],
        'allergies': ['mustard'],
        'activity_level_suitability': ['medium'],
        'ingredients': [
            'Idli batter (store-bought or homemade)', 'Coconut chutney', 'Sambar (optional)'
        ],
        'instructions': [
            'Grease idli molds. Pour batter into molds and steam for 10-12 minutes or until cooked through.',
            'Serve hot with coconut chutney and sambar (if using).'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=idli_chutney_link'
    },
    {
        'id': 25,
        'title': 'Cornflakes with milk',
        'image':'https://as2.ftcdn.net/jpg/02/09/54/11/1000_F_209541147_EeuElTsWuQBH7IbNEEOrb0BqMGqsfI4k.jpg',
        'diet': ['vegetarian'],
        'allergies': ['dairy', 'gluten'],
        'activity_level_suitability': ['low', 'medium'],
        'ingredients': [
            '1 cup cornflakes', '1 cup milk (dairy or plant-based)', '1 tbsp sugar (optional)',
            'Sliced fruits (optional)'
        ],
        'instructions': [
            'Pour cornflakes into a bowl. Add milk. Sweeten with sugar if desired.',
            'Add sliced fruits for extra nutrition. Serve immediately.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=cornflakes_milk_link'
    },
    {
        'id': 26,
        'title': 'Veg sandwich',
        'image': 'https://www.indianhealthyrecipes.com/wp-content/uploads/2024/05/vegetarian-club-sandwich-recipe.jpg',
        'diet': ['vegetarian'],
        'allergies': ['gluten', 'dairy'],
        'activity_level_suitability': ['medium'],
        'ingredients': [
            '2 slices bread', '1/4 cup sliced cucumber', '1/4 cup sliced tomato',
            '1/4 cup sliced onion', '2 lettuce leaves', '1 tbsp mayonnaise or green chutney',
            'Salt and pepper to taste'
        ],
        'instructions': [
            'Toast bread slices lightly. Spread mayonnaise or green chutney on one side of each slice.',
            'Layer lettuce, cucumber, tomato, and onion on one slice. Season with salt and pepper.',
            'Top with the other bread slice. Cut diagonally and serve.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=veg_sandwich_link'
    },
    {
        'id': 27,
        'title': 'Upma',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTY53aX95ngx4daNRLz5ykPUHXLCgUCB98Ltw&s',
        'diet': ['vegetarian', 'vegan'],
        'allergies': ['gluten', 'nuts'],
        'activity_level_suitability': ['medium'],
        'ingredients': [
            '1 cup semolina (rawa)', '2 cups water', '1 onion, chopped', '1 carrot, chopped',
            '1/4 cup green peas', '1 tsp mustard seeds', '1 tsp urad dal (split black gram)',
            '1 green chili, slit', 'Curry leaves', '1 tbsp oil', 'Salt to taste'
        ],
        'instructions': [
            'Dry roast semolina in a pan until fragrant. Set aside.',
            'Heat oil in the same pan. Add mustard seeds, urad dal, green chili, and curry leaves. Sauté until fragrant.',
            'Add chopped onion, carrot, and peas. Sauté until vegetables are tender.',
            'Add water and salt. Bring to a boil. Reduce heat to low, gradually add roasted semolina while stirring continuously to prevent lumps.',
            'Cover and cook for 5-7 minutes until water is absorbed and upma is cooked. Serve hot.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=upma_link'
    },
    {
        'id': 28,
        'title': 'Besan chilla',
        'image': 'https://www.indianveggiedelight.com/wp-content/uploads/2022/12/besan-chilla-recipe-featured.jpg',
        'diet': ['vegetarian', 'vegan', 'gluten-free'],
        'allergies': [],
        'activity_level_suitability': ['medium'],
        'ingredients': [
            '1 cup gram flour (besan)', '1/4 cup finely chopped onion', '1/4 cup finely chopped bell peppers',
            '2 tbsp chopped coriander', '1/2 tsp turmeric powder', '1/2 tsp red chili powder',
            'Pinch of asafoetida (hing)', 'Water as needed (approx. 1 cup)', 'Oil for cooking', 'Salt to taste'
        ],
        'instructions': [
            'In a bowl, combine besan, chopped onion, bell peppers, coriander, turmeric, chili powder, asafoetida, and salt.',
            'Gradually add water while whisking to form a smooth, lump-free batter of pouring consistency.',
            'Heat a non-stick pan and grease lightly with oil. Pour a ladleful of batter and spread it into a thin circle.',
            'Cook until edges crisp and bottom is golden. Flip and cook the other side. Serve hot with chutney or pickle.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=besan_chilla_link'
    },
    {
        'id': 29,
        'title': 'Chole with roti',
        'image': 'https://www.eitanbernath.com/wp-content/uploads/2018/03/Eitan-Bernath-Quick-Chana-Masala-with-Roti.jpeg',
        'diet': ['vegetarian'],
        'allergies': ['gluten'],
        'activity_level_suitability': ['medium', 'high'],
        'ingredients': [
            '1 cup chickpeas (chole), soaked overnight and boiled', '1 onion, chopped', '1 tomato, chopped',
            '1 tbsp ginger-garlic paste', '1 tsp chole masala', '1/2 tsp turmeric powder',
            '1/2 tsp red chili powder', '2 tbsp oil', 'Salt to taste', 'Water as needed',
            'Whole wheat flour for roti'
        ],
        'instructions': [
            'Heat oil in a pan, sauté onion until golden. Add ginger-garlic paste and cook for 1 minute.',
            'Add chopped tomato and cook until soft. Add turmeric, chili, and chole masala, cook for 2 minutes.',
            'Add boiled chickpeas and a little water. Simmer for 10-15 minutes until gravy thickens. Season with salt.',
            'Serve hot with freshly made rotis.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=chole_roti_link'
    },
    {
        'id': 30,
        'title': 'Dal tadka with rice',
        'image': 'https://i0.wp.com/upbeetanisha.com/wp-content/uploads/2024/01/IMG_9643.jpg?resize=768%2C1024&ssl=1',
        'diet': ['vegetarian', 'vegan', 'gluten-free'],
        'allergies': [],
        'activity_level_suitability': ['medium'],
        'ingredients': [
            '1/2 cup toor dal (split pigeon peas), rinsed', '3 cups water', '1/4 tsp turmeric powder',
            'Salt to taste', 'For Tadka: 1 tbsp ghee or oil', '1 tsp cumin seeds', '1 onion, chopped',
            '2 cloves garlic, minced', '1 green chili, slit', 'Pinch of asafoetida (hing)',
            'Fresh coriander for garnish', 'Basmati rice for serving'
        ],
        'instructions': [
            'Cook toor dal with water, turmeric, and salt until soft and mushy (pressure cooker or pot).',
            'For tadka: Heat ghee/oil in a small pan. Add cumin seeds. Once they splutter, add onion and sauté until golden.',
            'Add garlic, green chili, and asafoetida. Cook for 1 minute. Pour this tadka over the cooked dal.',
            'Mix well and garnish with fresh coriander. Serve hot with steamed rice.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=dal_tadka_rice_link'
    },
    {
        'id': 31,
        'title': 'Pulao with curd',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlXh32AHu69AsVM21AYdWBnVPXZJVy4DGhmw&s',
        'diet': ['vegetarian'],
        'allergies': ['dairy'],
        'activity_level_suitability': ['medium'],
        'ingredients': [
            '1 cup basmati rice, soaked', '2 cups mixed vegetables (peas, carrots, potatoes)',
            '1 onion, sliced', '1 tbsp ginger-garlic paste', '1 tsp whole spices',
            '1 tsp cumin seeds', '2 tbsp oil', 'Salt to taste', '2 cups water',
            '1 cup curd (yogurt)'
        ],
        'instructions': [
            'Prepare vegetable pulao as per recipe ID 23. Let it cool slightly.',
            'Serve the pulao hot with a side of plain curd (yogurt).'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=pulao_curd_link'
    },
    {
        'id': 32,
        'title': 'Bhindi sabzi with roti',
        'image': 'https://i0.wp.com/upbeetanisha.com/wp-content/uploads/2021/03/DSC_3693.jpg?resize=827%2C1024&ssl=1',
        'diet': ['vegetarian'],
        'allergies': ['gluten'],
        'activity_level_suitability': ['medium'],
        'ingredients': [
            '500g okra (bhindi), chopped', '1 onion, sliced', '1 tomato, chopped',
            '1 tsp ginger-garlic paste', '1 tsp coriander powder', '1/2 tsp turmeric powder',
            '1/2 tsp red chili powder', '2 tbsp oil', 'Salt to taste', 'Whole wheat flour for roti'
        ],
        'instructions': [
            'Heat oil in a pan, add bhindi and sauté until it\'s no longer sticky. Set aside.',
            'In the same pan, sauté onion until golden. Add ginger-garlic paste and cook for 1 minute.',
            'Add chopped tomato and cook until soft. Add all dry spices and cook for 2 minutes.',
            'Add the sautéed bhindi, mix well, and cook for 5-7 minutes or until tender-crisp. Season with salt.',
            'Serve hot with freshly made rotis.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=bhindi_sabzi_roti_link'
    },
    {
        'id': 33,
        'title': 'Vegetable korma',
        'image': 'https://www.indianhealthyrecipes.com/wp-content/uploads/2022/03/veg-kurma-vegetable-korma-recipe.jpg',
        'diet': ['vegetarian'],
        'allergies': ['dairy', 'nuts'],
        'activity_level_suitability': ['medium'],
        'ingredients': [
            '1 cup mixed vegetables (potatoes, carrots, peas, beans)', '1 onion, chopped',
            '1 tbsp ginger-garlic paste', '1/4 cup cashew paste or coconut paste', '1/2 cup curd (yogurt)',
            '1 tsp korma masala', '1/2 tsp turmeric powder', '2 tbsp oil', 'Salt to taste',
            '1/4 cup cream (optional)'
        ],
        'instructions': [
            'Heat oil in a pan, sauté onion until golden. Add ginger-garlic paste and cook for 1 minute.',
            'Add mixed vegetables and cook for 5 minutes. Add turmeric and korma masala, cook for 2 minutes.',
            'Whisk curd with cashew/coconut paste and add to the pan. Simmer until gravy thickens and vegetables are tender.',
            'Stir in cream (if using). Season with salt. Serve hot with rice or bread.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=veg_korma_link'
    },
    {
        'id': 34,
        'title': 'Stuffed capsicum',
        'image': 'https://assets.sweat.com/html_body_blocks/images/000/005/624/original/StuffedCapsicum_enefd376454d860e15efe0f560635f4d10.jpg?1565321138',
        'diet': ['vegetarian'],
        'allergies': [],
        'activity_level_suitability': ['medium'],
        'ingredients': [
            '2-3 bell peppers (capsicum)', '1 cup mashed boiled potatoes', '1/2 cup green peas',
            '1/4 cup chopped onion', '1 tbsp ginger-garlic paste', '1 tsp garam masala',
            '1/2 tsp turmeric powder', '2 tbsp oil', 'Salt to taste'
        ],
        'instructions': [
            'Halve bell peppers and remove seeds. Blanch in boiling water for 2-3 minutes. Set aside.',
            'Heat oil in a pan, sauté onion until golden. Add ginger-garlic paste, cook for 1 minute.',
            'Add mashed potatoes, green peas, turmeric, garam masala, and salt. Mix well and cook for 5 minutes.',
            'Stuff the bell peppers with the potato mixture. Arrange in a baking dish.',
            'Bake at 180°C (350°F) for 20-25 minutes, or until capsicum is tender. Serve hot.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=stuffed_capsicum_link'
    },
    {
        'id': 35,
        'title': 'Veg noodles',
        'image': 'https://shwetainthekitchen.com/wp-content/uploads/2023/03/vegetable-noodles.jpg',
        'diet': ['vegetarian', 'vegan'],
        'allergies': ['gluten'],
        'activity_level_suitability': ['medium', 'high'],
        'ingredients': [
            '200g noodles', '1 cup sliced cabbage', '1/2 cup sliced carrots',
            '1/2 cup sliced bell peppers', '2 tbsp soy sauce', '1 tbsp vinegar',
            '1 tsp ginger-garlic paste', '2 tbsp oil', 'Salt and pepper to taste'
        ],
        'instructions': [
            'Cook noodles according to package directions. Drain and rinse with cold water to prevent sticking.',
            'Heat oil in a wok or large pan over high heat. Add ginger-garlic paste and sauté for 30 seconds.',
            'Add all sliced vegetables and stir-fry for 3-5 minutes until tender-crisp.',
            'Add cooked noodles, soy sauce, vinegar, salt, and pepper. Toss well to combine.',
            'Cook for another 2-3 minutes, ensuring everything is well mixed and hot. Serve hot.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=veg_noodles_link'
    },
    {
        'id': 36,
        'title': 'Rajma with brown rice',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQtM20qayB8Ef9lF_Q2syBKrwr8w0awYFohmQ&s',
        'diet': ['vegetarian', 'vegan', 'gluten-free'],
        'allergies': [],
        'activity_level_suitability': ['medium', 'high'],
        'ingredients': [
            '1 cup kidney beans (rajma), soaked overnight and boiled', '1 onion, chopped', '1 tomato, chopped',
            '1 tbsp ginger-garlic paste', '1 tsp cumin powder', '1 tsp coriander powder',
            '1/2 tsp turmeric powder', '1/2 tsp red chili powder', '2 tbsp oil', 'Salt to taste',
            'Brown rice for serving'
        ],
        'instructions': [
            'Heat oil in a pan, sauté onion until golden. Add ginger-garlic paste and cook for 1 minute.',
            'Add chopped tomato and cook until soft. Add all dry spices and cook for 2 minutes.',
            'Add boiled rajma and a little water. Simmer for 15-20 minutes until gravy thickens. Season with salt.',
            'Serve hot with cooked brown rice.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=rajma_brown_rice_link'
    },
    {
        'id': 37,
        'title': 'Kadhi chawal',
        'image': 'https://www.scrumptiously.com/wp-content/uploads/2024/06/KadhiChawal.webp',
        'diet': ['vegetarian'],
        'allergies': ['dairy', 'gluten'],
        'activity_level_suitability': ['medium'],
        'ingredients': [
            '1/2 cup gram flour (besan)', '1 cup sour curd (yogurt)', '4 cups water',
            '1 tsp turmeric powder', '1 tsp red chili powder', 'Salt to taste',
            'For Tadka: 1 tbsp ghee or oil', '1 tsp cumin seeds', '1/2 tsp fenugreek seeds',
            'Pinch of asafoetida', 'Dry red chilies', 'Curry leaves', 'Steamed rice for serving'
        ],
        'instructions': [
            'In a large bowl, whisk besan with curd until smooth. Gradually add water, turmeric, chili powder, and salt, mixing well to form a lump-free batter.',
            'Pour batter into a pot and bring to a boil over medium heat, stirring continuously to prevent curdling. Reduce heat and simmer for 15-20 minutes until kadhi thickens.',
            'For tadka: Heat ghee/oil. Add cumin seeds, fenugreek seeds, asafoetida, dry red chilies, and curry leaves. Once fragrant, pour over the simmering kadhi.',
            'Mix well and serve hot with steamed rice.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=kadhi_chawal_link'
    },
    {
        'id': 38,
        'title': 'Spinach dal',
        'image': 'https://rainbowplantlife.com/wp-content/uploads/2024/05/Dal-Palak-hero-shots-3-of-4.jpg',
        'diet': ['vegetarian', 'vegan', 'gluten-free'],
        'allergies': [],
        'activity_level_suitability': ['medium'],
        'ingredients': [
            '1/2 cup mixed lentils (toor, moong)', '1 cup chopped spinach', '3 cups water',
            '1 onion, chopped', '1 tomato, chopped', '1 tbsp ginger-garlic paste',
            '1 tsp cumin powder', '1/2 tsp turmeric powder', '2 tbsp oil', 'Salt to taste'
        ],
        'instructions': [
            'Wash lentils and combine with water, turmeric, and salt in a pressure cooker. Cook for 2-3 whistles or until tender.',
            'Heat oil in a separate pan. Sauté onion until golden. Add ginger-garlic paste and tomato, cook until soft.',
            'Add cumin powder and chopped spinach. Cook until spinach wilts.',
            'Add the cooked dal to the spinach mixture. Simmer for 5-7 minutes. Season with salt. Serve hot.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=spinach_dal_link'
    },

    # High Activity Meals
    {
        'id': 39,
        'title':'Partha with curd',
        'image': 'https://i.redd.it/j7bt3tm71gmc1.jpeg',
        'diet': ['vegetarian'],
        'allergies': ['gluten', 'dairy'],
        'activity_level_suitability': ['high'],
        'ingredients': [
            'Whole wheat flour for parathas', 'Water and salt for dough', 'Ghee or oil for cooking',
            '1 cup curd (yogurt)', 'Pinch of roasted cumin powder (optional)'
        ],
        'instructions': [
            'Prepare a soft dough using whole wheat flour, water, and salt. Roll out thin parathas.',
            'Cook parathas on a hot griddle with ghee/oil until golden brown spots appear on both sides.',
            'Serve hot parathas with a side of plain curd, optionally seasoned with cumin powder.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=paratha_curd_link'
    },
    {
        'id': 40,
        'title': 'Banana peanut butter sandwich',
        'image': 'https://www.eatingwell.com/thmb/Aw0khvLDnRh0CdI4pv3eu6AdHaM=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/5180292-b58d1690f4bb41f2a5e5d6f34de10080.jpg',
        'diet': ['vegetarian', 'vegan'],
        'allergies': ['gluten', 'peanuts'],
        'activity_level_suitability': ['high'],
        'ingredients': [
            '2 slices whole wheat bread', '2 tbsp peanut butter', '1 medium banana, sliced'
        ],
        'instructions': [
            'Toast bread slices if desired. Spread peanut butter evenly on both slices.',
            'Arrange banana slices on one slice, then top with the other. Cut diagonally and serve.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=9uwfdL_oXLQ'
    },
    {
        'id': 41,
        'title': 'Omelette with toast',
        'image': 'https://recipesblob.oetker.in/assets/bed50b6fbbb84fc0ae786136d5351af4/750x910/bread-omelette.jpg',
        'diet': ['non-vegetarian'],
        'allergies': ['gluten', 'dairy'],
        'activity_level_suitability': ['high'],
        'ingredients': [
            '3 large eggs', '2 tbsp milk or water', '1/4 cup chopped onion (optional)',
            '1/4 cup chopped bell peppers (optional)', '1 tbsp oil or butter',
            'Salt and pepper to taste', '2 slices whole wheat toast'
        ],
        'instructions': [
            'In a bowl, whisk eggs with milk/water, salt, and pepper. Add chopped onion and bell peppers if desired.',
            'Heat oil/butter in a non-stick skillet. Pour egg mixture and cook until set.',
            'Fold the omelette in half and slide onto a plate. Serve immediately with toast.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=vMpGXlYKr64'
    },
    {
        'id': 42,
        'title': 'Moong dal chilla',
        'image': 'https://www.cubesnjuliennes.com/wp-content/uploads/2018/09/Moong-Palak-Cheela-recipe.jpg',
        'diet': ['vegetarian', 'vegan', 'gluten-free'],
        'allergies': [],
        'activity_level_suitability': ['high'],
        'ingredients': [
            '1 cup yellow split lentils (moong dal), soaked overnight', '1 inch ginger',
            '1-2 green chilies', '1/4 cup chopped onion', '2 tbsp chopped coriander',
            '1/2 tsp cumin powder', 'Water as needed', 'Oil for cooking', 'Salt to taste'
        ],
        'instructions': [
            'Drain soaked moong dal. Blend with ginger and green chilies, adding a little water to make a smooth batter.',
            'Transfer to a bowl. Add chopped onion, coriander, cumin powder, and salt. Mix well.',
            'Heat a non-stick pan and grease lightly. Pour a ladleful of batter and spread into a thin circle.',
            'Cook until golden brown and crisp on both sides. Serve hot with chutney.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=DBhBE_xqZJ4'
    },
    {
        'id': 43,
        'title': 'Paneer bhurji',
        'image': 'https://www.cookwithmanali.com/wp-content/uploads/2019/06/Paneer-Bhurji-Recipe-Vegetarian-Indian-Cottage-Cheese-Scramble.jpg',
        'diet': ['vegetarian'],
        'allergies': ['dairy'],
        'activity_level_suitability': ['high'],
        'ingredients': [
            '200g paneer, crumbled', '1 onion, finely chopped', '1 tomato, finely chopped',
            '1 tbsp ginger-garlic paste', '1/2 tsp turmeric powder', '1 tsp coriander powder',
            '1/2 tsp red chili powder', '1/2 tsp garam masala', '2 tbsp oil',
            'Salt to taste', 'Fresh coriander for garnish'
        ],
        'instructions': [
            'Heat oil in a pan. Sauté onion until golden. Add ginger-garlic paste and cook for 1 minute.',
            'Add chopped tomato and cook until soft. Add turmeric, coriander, chili powder, and garam masala. Cook for 2 minutes.',
            'Add crumbled paneer and mix well. Cook for 5-7 minutes, stirring occasionally, until dry and well combined. Season with salt.',
            'Garnish with fresh coriander. Serve hot with roti or bread.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=UhS1V6bYhVI'
    },
    {
        'id': 44,
        'title': 'Paneer curry with rice',
        'image': 'https://skinnyspatula.com/wp-content/uploads/2022/01/Paneer_Butter_Masala5.jpg',
        'diet': ['vegetarian'],
        'allergies': ['dairy', 'nuts'],
        'activity_level_suitability': ['high'],
        'ingredients': [
            '200g paneer, cubed', '1 onion, chopped', '1 tomato, chopped', '1 tbsp ginger-garlic paste',
            '1/4 cup cashew paste (optional)', '1 tsp garam masala', '1 tsp red chili powder',
            '1/2 tsp turmeric powder', '2 tbsp oil', 'Salt to taste', 'Water as needed', 'Rice for serving'
        ],
        'instructions': [
            'Heat oil in a pan, lightly fry paneer cubes until golden, set aside. In the same oil, sauté onion until golden.',
            'Add ginger-garlic paste, cook for 1 minute. Add chopped tomato and cook until soft.',
            'Add turmeric, chili powder, garam masala, and cashew paste (if using). Cook for 2 minutes.',
            'Add water to adjust gravy consistency. Bring to a simmer. Add fried paneer and cook for 5-7 minutes.',
            'Season with salt. Serve hot with steamed rice.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=5HLpfiPPdqw'
    },
    {
        'id': 45,
        'title': 'Egg biryani',
        'image': 'https://palatesdesire.com/wp-content/uploads/2022/05/Egg-biryani-recipe@palates-desire.jpg',
        'diet': ['non-vegetarian'],
        'allergies': ['dairy'],
        'activity_level_suitability': ['high'],
        'ingredients': [
            '4-5 boiled eggs', '1 cup basmati rice, soaked', '1 onion, sliced and fried until crispy (birista)',
            '1 tomato, chopped', '1 tbsp ginger-garlic paste', '1/2 cup curd (yogurt)',
            '2 tbsp biryani masala', 'Mint and coriander leaves', '2 tbsp oil/ghee',
            'Salt to taste', 'Water as needed'
        ],
        'instructions': [
            'Cook soaked basmati rice until 70% done. Drain and set aside.',
            'Heat oil/ghee in a pan. Sauté onion slices until golden brown and crispy (birista). Remove half for garnish.',
            'Add ginger-garlic paste, tomato, and cook until soft. Add biryani masala, turmeric, and curd. Cook until oil separates.',
            'Add boiled eggs and cook for 5 minutes. In a heavy-bottomed pot, layer half the rice, then the egg masala, then remaining rice.',
            'Garnish with remaining birista, mint, and coriander. Cover tightly and cook on low heat for 15-20 minutes (dum cooking). Serve hot.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=LTJWBzOwuIE'
    },
    {
        'id': 46,
        'title': 'Mixed dal with jeera rice',
        'image': 'https://madresfoods.com/cdn/shop/files/ArharDalandJeeraRice-min.png?v=1715773676',
        'diet': ['vegetarian', 'vegan', 'gluten-free'],
        'allergies': [],
        'activity_level_suitability': ['high'],
        'ingredients': [
            '1 cup mixed lentils (toor, masoor, chana), rinsed', '3 cups water', '1/2 tsp turmeric powder',
            'Salt to taste', 'For Jeera Rice: 1 cup basmati rice', '2 cups water', '1 tbsp ghee or oil',
            '1 tsp cumin seeds', 'Salt to taste', 'For Dal Tadka: 1 tbsp ghee or oil',
            '1 tsp cumin seeds', '1 onion, chopped', '2 cloves garlic, minced', '1 green chili, slit'
        ],
        'instructions': [
            'Cook mixed lentils with water, turmeric, and salt until soft. Prepare tadka and mix into dal as per recipe ID 30.',
            'For Jeera Rice: Wash rice. Heat ghee/oil in a pot. Add cumin seeds. When spluttering, add rice, water, and salt. Bring to a boil, then simmer until water is absorbed and rice is cooked.',
            'Serve hot mixed dal with hot jeera rice.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=kCi8bsJVtcY'
    },
    {
        'id': 47,
        'title': 'Chicken pulao',
        'image': 'https://www.funfoodfrolic.com/wp-content/uploads/2020/07/Chicken-Pulao-Thumbnail.jpg',
        'diet': ['non-vegetarian'],
        'allergies': [],
        'activity_level_suitability': ['high'],
        'ingredients': [
            '500g chicken, cut into pieces', '1 cup basmati rice, soaked', '1 onion, sliced',
            '1 tbsp ginger-garlic paste', '2 tbsp chicken pulao masala', '1/2 cup curd (yogurt)',
            '2 tbsp oil', 'Salt to taste', '2 cups water'
        ],
        'instructions': [
            'Heat oil in a pot, sauté onion until golden. Add ginger-garlic paste and chicken pieces. Cook until chicken is lightly browned.',
            'Add chicken pulao masala, curd, and salt. Cook for 5-7 minutes.',
            'Add soaked rice and water. Bring to a boil, then reduce heat, cover, and cook until water is absorbed and rice is tender. Serve hot.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=CQabDPkh1J0'
    },
    {
        'id': 48,
        'title': 'Soya chunk curry',
        'image': 'https://foodiesterminal.com/wp-content/uploads/2020/01/soya-chunks-curry-5-678x1024.jpg',
        'diet': ['vegetarian', 'vegan'],
        'allergies': ['soy'],
        'activity_level_suitability': ['high'],
        'ingredients': [
            '1 cup soya chunks, soaked and squeezed dry', '1 onion, chopped', '1 tomato, chopped',
            '1 tbsp ginger-garlic paste', '1 tsp garam masala', '1 tsp red chili powder',
            '1/2 tsp turmeric powder', '2 tbsp oil', 'Salt to taste', 'Water as needed'
        ],
        'instructions': [
            'Heat oil in a pan, sauté onion until golden. Add ginger-garlic paste and cook for 1 minute.',
            'Add chopped tomato and cook until soft. Add turmeric, chili powder, garam masala. Cook for 2 minutes.',
            'Add soaked soya chunks and a little water. Simmer for 10-15 minutes until gravy thickens. Season with salt.',
            'Serve hot with rice or roti.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=PcxKLW8COZ8'
    },
    {
        'id': 49,
        'title': 'Rajma chawal',
        'image': 'https://www.secondrecipe.com/wp-content/uploads/2017/08/rajma-chawal-1.jpg',
        'diet': ['vegetarian', 'vegan', 'gluten-free'],
        'allergies': [],
        'activity_level_suitability': ['high'],
        'ingredients': [
            '1 cup kidney beans (rajma), soaked overnight and boiled', '1 onion, chopped', '1 tomato, chopped',
            '1 tbsp ginger-garlic paste', '1 tsp cumin powder', '1 tsp coriander powder',
            '1/2 tsp turmeric powder', '1/2 tsp red chili powder', '2 tbsp oil', 'Salt to taste',
            'Basmati rice for serving'
        ],
        'instructions': [
            'Prepare rajma curry as per recipe ID 36. Cook basmati rice separately. Serve hot rajma curry with hot rice.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=elR-v9M86Ls'
    },
    {
        'id': 50,
        'title': 'Fish curry with rice',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQGJot_JieyQXn-m9SBbjOmlWnDzcqTZnhJXA&s',
        'diet': ['non-vegetarian'],
        'allergies': ['fish'],
        'activity_level_suitability': ['high'],
        'ingredients': [
            '500g fish fillets (e.g., cod, tilapia), cut into pieces', '1 onion, chopped', '1 tomato, chopped',
            '1 tbsp ginger-garlic paste', '2 tbsp fish curry powder', '1/2 cup coconut milk (optional)',
            '2 tbsp oil', 'Salt to taste', 'Water as needed', 'Rice for serving'
        ],
        'instructions': [
            'Heat oil in a pan, sauté onion until golden. Add ginger-garlic paste and cook for 1 minute.',
            'Add chopped tomato and cook until soft. Add fish curry powder and a little water, cook for 2 minutes.',
            'Add fish pieces and gently mix. Add coconut milk (if using) and enough water to make gravy. Simmer for 10-12 minutes until fish is cooked through.',
            'Season with salt. Serve hot with steamed rice.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=GJsQjUuYe8w'
    },
    {
        'id': 51,
        'title': 'Matar paneer with roti',
        'image': 'https://www.simplyrecipes.com/thmb/Th15MyYH39AyYVe3Yy1uuXMp1E0=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Matar-Paneer-LEAD-04-54973561cdb944f587165ecf161acc83.jpg',
        'diet': ['vegetarian'],
        'allergies': ['dairy', 'gluten'],
        'activity_level_suitability': ['high'],
        'ingredients': [
            '200g paneer, cubed', '1 cup green peas (matar)', '1 onion, chopped', '1 tomato, chopped',
            '1 tbsp ginger-garlic paste', '1 tsp garam masala', '1 tsp red chili powder',
            '1/2 tsp turmeric powder', '2 tbsp oil', 'Salt to taste', 'Water as needed', 'Whole wheat flour for roti'
        ],
        'instructions': [
            'Heat oil in a pan, lightly fry paneer cubes until golden, set aside. In the same oil, sauté onion until golden.',
            'Add ginger-garlic paste and cook for 1 minute. Add chopped tomato and cook until soft.',
            'Add turmeric, chili powder, garam masala. Cook for 2 minutes. Add green peas and a little water. Cook for 5 minutes.',
            'Add fried paneer and water to adjust gravy consistency. Simmer for 5-7 minutes. Season with salt.',
            'Serve hot with freshly made rotis.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=fA9Z8nb_z0Y'
    },
    {
        'id': 52,
        'title': 'Stuffed paratha with salad',
        'image': 'https://www.archanaskitchen.com/images/archanaskitchen/0-Archanas-Kitchen-Recipes/2018/Jan_-16/Dinner_Plate_Raw_Papaya_Red_Capsicum_Stuffed_Paratha_Carrot_Salad_Makhana_Raita_Vivatta-1.jpg',
        'diet': ['vegetarian'],
        'allergies': ['gluten', 'dairy'],
        'activity_level_suitability': ['high'],
        'ingredients': [
            'Whole wheat flour for parathas', 'Water and salt for dough', 'For stuffing: mashed spiced potatoes/paneer',
            'Ghee or oil for cooking', 'For salad: cucumber, tomato, onion, lemon, salt'
        ],
        'instructions': [
            'Prepare a soft dough. Prepare stuffing (e.g., mashed potatoes with spices).',
            'Roll out a small disc of dough, place stuffing, seal, and roll again into a paratha. Cook on a griddle with ghee/oil until golden brown.',
            'For salad: chop cucumber, tomato, onion. Season with salt and lemon juice.',
            'Serve hot stuffed paratha with the fresh salad.'
        ],
        'youtube_link': 'https://www.youtube.com/watch?v=nZP-wtZH08E'
    }
]
