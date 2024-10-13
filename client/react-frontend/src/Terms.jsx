function Terms() {
    return (
        <div className="max-w-4xl px-4 py-8 mx-auto bg-white rounded-lg shadow-lg">
            <h1 className="mb-6 text-3xl font-bold text-gray-800">Terms and Conditions</h1>
            <p className="mb-6 text-gray-600">Welcome to Truth of the Platter. By using our service, you agree to the following terms and conditions:</p>
            
            {[
                {
                    title: "1. Service Description",
                    content: "Truth of the Platter is a web application that aggregates restaurant reviews from multiple sources, including Yelp, TripAdvisor, and Google, to provide a more comprehensive rating."
                },
                {
                    title: "2. Use of Third-Party Data",
                    content: "Our service utilizes data from Yelp, Google, and TripAdvisor to gather restaurant information. By using Truth of the Platter, you agree to comply with the terms of service of these third-party providers. The data displayed on Truth of the Platter is sourced from these providers and remains their property. We do not claim ownership of this data."
                },
                {
                    title: "3. Use of Third-Party Trademarks and Logos",
                    content: "Truth of the Platter may display trademarks, logos, and other proprietary information belonging to third parties, including but not limited to Yelp, Google, and TripAdvisor. These trademarks and logos are used for identification purposes only and remain the exclusive property of their respective owners. Their use does not imply endorsement or affiliation with Truth of the Platter."
                },
                {
                    title: "4. Accuracy of Information",
                    content: "While we strive to provide accurate and up-to-date information, the ratings, reviews, and other data displayed on Truth of the Platter are sourced from third parties and are not guaranteed to be accurate or complete. Users should consider this information as a guide and not as definitive facts. Truth of the Platter does not independently verify the accuracy of the data provided by third-party sources."
                },
                {
                    title: "5. Use of Location Data",
                    content: "Truth of the Platter may request access to your device's location data to provide location-based services, such as finding nearby restaurants. We only access your location when you grant permission and while you are using the app. You can revoke this permission at any time through your device settings. We do not store your precise location data on our servers or share it with third parties."
                },
                {
                    title: "6. Limitations of Liability",
                    content: "Truth of the Platter is not responsible for any decisions made based on the information provided by our service. Users should use their own judgment when making decisions based on the aggregated reviews and ratings."
                },
                {
                    title: "7. Intellectual Property",
                    content: "The content, design, and functionality of Truth of the Platter are protected by copyright and other intellectual property laws. Users may not reproduce, distribute, or create derivative works without our express permission."
                },
                {
                    title: "8. Privacy",
                    content: "We respect your privacy and handle your data in accordance with our Privacy Policy. By using Truth of the Platter, you consent to our collection and use of data as described in the Privacy Policy."
                },
                {
                    title: "9. Modifications to the Service",
                    content: "We reserve the right to modify, suspend, or discontinue Truth of the Platter at any time without notice. We are not liable to you or any third party for any modification, suspension, or discontinuation of the service."
                },
                {
                    title: "10. Contact Information",
                    content: "If you have any questions about these Terms and Conditions, please contact us at noahlandis980@gmail.com."
                }
            ].map((section, index) => (
                <div key={index} className="mb-6">
                    <h2 className="mb-2 text-xl font-semibold text-gray-700">{section.title}</h2>
                    <p className="text-gray-600">{section.content}</p>
                </div>
            ))}
        </div>
    );
}

export default Terms;
