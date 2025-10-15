# Frontend Interface for AI Recommender

This directory contains all the client-side code for the AI Product Recommender. It is a dynamic, single-page interface built with vanilla HTML, CSS, and JavaScript that communicates with the backend API to display personalized recommendations in a stunning, modern UI.

---

## 🎨 Key Features

-   **Advanced Aurora UI:** The interface features a beautiful, animated aurora gradient background with soft, drifting shapes, creating an elegant and futuristic user experience.
-   **Minimalist Dark Theme:** A clean, near-black theme makes the content and glowing visual effects pop.
-   **Refined Card Design:** Product cards are clean and minimalist, with a subtle border that lights up with a soft glow on hover.
-   **Smooth Transitions & Animations:** All elements, from the button to the recommendation cards, feature polished transitions and staggered fade-in animations for a satisfying and high-quality feel.
-   **Dynamic Content:** Recommendations are fetched from the backend and rendered on the page without a refresh. An animated loader provides a smooth user experience during the fetch process.
-   **Automatic User Identity:** The application relies on the browser's cookie management to interact with the backend, requiring no user input to identify them.

---

## 💻 Technology Stack

-   **HTML5:** Provides the core structure of the web page.
-   **CSS3:** Handles all styling, including the aurora background, card design, animations, and responsive layout.
-   **Vanilla JavaScript:** Powers all client-side logic, including API calls and dynamic HTML manipulation. No external frameworks are used.

---

## ⚙️ How It Works

1.  **Event Listener:** An event listener is attached to the "Generate My Recommendations" button.
2.  **API Call:** When clicked, the JavaScript makes a `fetch` request to the backend's `/recommendations` endpoint.
    -   Crucially, it includes the `credentials: 'include'` option, which tells the browser to automatically send the `user_id` cookie with the request.
3.  **Render Results:** The script parses the JSON response from the server.
4.  **Dynamic HTML:** For each recommended product, it dynamically creates an HTML card element—including the image, title, AI explanation, and platform links—and appends it to the main container.

---

## ▶️ How to Run

Since this is a static frontend, no build process is required.

1.  Ensure the backend server is running.
2.  Open the `index.html` file directly in any modern web browser.

For a better development experience, you can use a live server extension, such as the **Live Server** extension for Visual Studio Code, which automatically reloads the page when you save a file.