export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary to-blue-700 text-white py-20">
        <div className="container">
          <div className="max-w-2xl">
            <h1 className="text-5xl font-bold mb-6">Learn Anything, Anytime, Anywhere</h1>
            <p className="text-xl mb-8 text-blue-100">
              Access world-class courses taught by industry experts. Start your learning journey
              today.
            </p>
            <div className="flex gap-4">
              <a
                href="/register"
                className="btn-primary inline-block"
              >
                Get Started
              </a>
              <a
                href="/courses"
                className="inline-block px-6 py-3 border-2 border-white rounded-lg font-semibold hover:bg-white hover:text-primary transition-all"
              >
                Explore Courses
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container">
          <h2 className="text-4xl font-bold text-center mb-12">Why Choose EduLearn?</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: '🎓',
                title: 'Expert Instructors',
                description: 'Learn from industry professionals with years of experience',
              },
              {
                icon: '📱',
                title: 'Learn at Your Pace',
                description: 'Study whenever and wherever you want, at your own speed',
              },
              {
                icon: '🏆',
                title: 'Certificates',
                description: 'Earn recognized certificates upon course completion',
              },
              {
                icon: '💰',
                title: 'Affordable Pricing',
                description: 'High-quality education at competitive prices',
              },
              {
                icon: '🤝',
                title: 'Community Support',
                description: 'Connect with fellow learners and get support',
              },
              {
                icon: '📊',
                title: 'Track Progress',
                description: 'Monitor your learning progress with detailed analytics',
              },
            ].map((feature, index) => (
              <div key={index} className="card text-center">
                <div className="text-5xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary text-white py-16">
        <div className="container text-center">
          <h2 className="text-3xl font-bold mb-6">Ready to Start Learning?</h2>
          <a href="/register" className="btn-primary inline-block">
            Sign Up Now
          </a>
        </div>
      </section>
    </main>
  )
}
