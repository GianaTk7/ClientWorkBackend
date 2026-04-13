import React from 'react';
import Layout from '../components/Layout';

const Services = () => {
  const services = [
    {
      name: "Braiding",
      description: "Our skilled braiders create intricate, stylish, and long-lasting braid designs tailored to your preferences. From box braids to cornrows, each style is crafted with precision, ensuring your hair looks flawless and healthy."
    },
    {
      name: "Wigs Installation",
      description: "We provide professional wig installation and styling to give you a seamless, natural look. Whether you want a protective style or a complete transformation, our team ensures your wig fits perfectly and complements your style."
    },
    {
      name: "Loc Styling & Maintenance",
      description: "Maintain and style your locs with our expert care. We offer retwists, loc extensions, and creative styling options that keep your locs healthy, neat, and full of personality."
    },
    {
      name: "Natural Hair Styling",
      description: "Embrace your natural beauty with our specialized natural hair services. From twist-outs to protective styles, we focus on enhancing your hair’s health while giving it a stunning, polished look."
    },
    {
      name: "Braiding Consultations",
      description: "Not sure which style suits you best? Our stylists provide consultations to recommend styles based on your hair type, face shape, and lifestyle. We'll help you choose a look you'll love and maintain with ease."
    }
  ];

  return (
    <Layout>
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem' }}>
        <h1 style={{ textAlign: 'center', fontSize: '2.5rem', marginBottom: '4rem', color: '#ec489a' }}>
          Our Services
        </h1>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
          {services.map((service, index) => (
            <div
              key={index}
              style={{
                padding: '2rem',
                background: 'white',
                borderRadius: '1rem',
                boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
                transition: 'transform 0.3s, box-shadow 0.3s',
              }}
              className="service-card"
            >
              <h3 style={{ fontSize: '1.75rem', marginBottom: '1rem', color: '#111827' }}>
                {service.name}
              </h3>
              <p style={{ fontSize: '1rem', color: '#4b5563', lineHeight: '1.6' }}>
                {service.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Call-to-Action */}
      <section style={{ marginTop: '4rem', textAlign: 'center', padding: '2rem', background: '#fdf2f8', borderRadius: '1rem' }}>
        <h2 style={{ fontSize: '2rem', color: '#ec489a', marginBottom: '1rem' }}>Ready to Transform Your Hair?</h2>
        <p style={{ fontSize: '1.125rem', color: '#6b7280', marginBottom: '1.5rem' }}>
          Book an appointment with our expert braiders and give your hair the care and style it deserves.
        </p>
        <a
          href="/booking"
          style={{
            display: 'inline-block',
            background: 'linear-gradient(90deg, #ec489a 0%, #8b5cf6 100%)',
            color: 'white',
            padding: '0.75rem 2rem',
            borderRadius: '9999px',
            fontWeight: '600',
            textDecoration: 'none',
            transition: 'background 0.3s',
          }}
          onMouseEnter={e => (e.currentTarget.style.background = 'linear-gradient(90deg, #f472b6 0%, #a78bfa 100%)')}
          onMouseLeave={e => (e.currentTarget.style.background = 'linear-gradient(90deg, #ec489a 0%, #8b5cf6 100%)')}
        >
          Book Your Appointment
        </a>
      </section>
    </Layout>
  );
};

export default Services;