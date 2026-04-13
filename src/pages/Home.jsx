import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  SparklesIcon, 
  ClockIcon, 
  StarIcon, 
  HeartIcon, 
  ScissorsIcon, 
  FaceSmileIcon 
} from '@heroicons/react/24/outline';
import Layout from '../components/Layout';

const Home = () => {
  const features = [
    {
      icon: SparklesIcon,
      title: "Expert Stylists",
      description: "Our team of professional stylists stays updated with the latest trends",
      color: "from-pink-500 to-rose-500"
    },
    {
      icon: ClockIcon,
      title: "Easy Booking",
      description: "Book your appointment online in just a few clicks, 24/7",
      color: "from-purple-500 to-indigo-500"
    },
    {
      icon: StarIcon,
      title: "Premium Products",
      description: "We use only high-quality, professional products for the best results",
      color: "from-yellow-500 to-orange-500"
    },
    {
      icon: HeartIcon,
      title: "Relaxing Atmosphere",
      description: "Enjoy a luxurious and comfortable environment during your visit",
      color: "from-teal-500 to-emerald-500"
    }
  ];

 const services = [
  { 
    name: "Hair Styling", 
    icon: ScissorsIcon,
    description: "Expert cuts, blowouts, and styling for any occasion",
    features: ["Women's Cuts", "Men's Cuts", "Kids' Cuts", "Blowouts", "Updos", "Special Occasion Styling"]
  },

  { 
    name: "Wigs Installation", 
    icon: FaceSmileIcon,
    description: "Professional wig fitting, styling, and maintenance",
    features: ["Lace Front Wigs", "Full Lace Wigs", "Wig Customization", "Wig Cutting & Styling", "Wig Maintenance", "Adhesive Application"]
  },
  { 
    name: "Braiding & Twisting", 
    icon: StarIcon,
    description: "Protective styles that are both beautiful and healthy for your hair",
    features: ["Box Braids", "Cornrows", "Twist Styles", "Faux Locs", "Feed-in Braids", "Knotless Braids"]
  },
  { 
    name: "Relaxing hair", 
    icon: HeartIcon,
    description: "Specialized care for natural and textured hair",
    features: ["Wash & Go", "Deep Conditioning", "Trims", "Protective Styling", "Scalp Treatments", "Hydration Therapy"]
  },

];

  return (
    <Layout>
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-28">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h1 className="text-5xl md:text-6xl font-playfair font-bold leading-tight">
                <span className="bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent">
                  Transform Your Look
                </span>
                <br />
                <span className="text-gray-800">with Esther's salon</span>
              </h1>
              <p className="text-xl text-gray-600 mt-6 leading-relaxed">
                Experience luxury beauty services tailored just for you. From trendy haircuts to elegant styling,
                we make you feel beautiful and confident.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 mt-8">
                <Link to="/booking" className="btn-primary text-center">
                  Book Appointment
                </Link>
                <Link to="/services" className="btn-secondary text-center">
                  View Services
                </Link>
              </div>
              
              {/* Stats */}
              <div className="flex gap-8 mt-12">
                <div>
                  <p className="text-3xl font-bold text-pink-600">500+</p>
                  <p className="text-gray-600">Happy Clients</p>
                </div>
                <div>
                  <p className="text-3xl font-bold text-purple-600">50+</p>
                  <p className="text-gray-600">Expert Stylists</p>
                </div>
                <div>
                  <p className="text-3xl font-bold text-orange-500">8</p>
                  <p className="text-gray-600">Years Experience</p>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6 }}
              className="relative"
            >
              <div className="relative rounded-2xl overflow-hidden shadow-2xl">
                <img
                  src="https://images.unsplash.com/photo-1560066984-138dadb4c035?ixlib=rb-4.0.3"
                  alt="Salon"
                  className="w-full h-auto"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
              </div>
              <motion.div
                animate={{ y: [0, -10, 0] }}
                transition={{ duration: 3, repeat: Infinity }}
                className="absolute -bottom-6 -left-6 bg-white rounded-2xl p-4 shadow-xl"
              >
                <div className="flex items-center space-x-2">
                  <StarIcon className="w-5 h-5 text-yellow-400 fill-current" />
                  <span className="font-bold">4.9/5</span>
                  <span className="text-gray-600">(150+ reviews)</span>
                </div>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl font-playfair font-bold text-gray-800 mb-4">
              Why Choose Us
            </h2>
            <p className="text-xl text-gray-600">
              Experience the difference with our premium services
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="card p-6 text-center hover:scale-105"
              >
                <div className={`w-16 h-16 bg-gradient-to-r ${feature.color} rounded-full flex items-center justify-center mx-auto mb-4`}>
                  <feature.icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-bold text-gray-800 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Services Preview */}
      <section className="py-20 bg-gradient-to-r from-pink-50 to-purple-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl font-playfair font-bold text-gray-800 mb-4">
              Our Popular Services
            </h2>
            <p className="text-xl text-gray-600">
              Discover our most loved treatments
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {services.map((service, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="card p-6"
              >
                <div className="w-12 h-12 bg-gradient-to-r from-pink-500 to-purple-500 rounded-full flex items-center justify-center mb-4">
                  <service.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-bold text-gray-800 mb-2">{service.name}</h3>
                <p className="text-2xl font-bold text-pink-600 mb-1">{service.price}</p>
                <p className="text-gray-500 text-sm">{service.duration}</p>
              </motion.div>
            ))}
          </div>

          <div className="text-center mt-12">
            <Link to="/services" className="btn-primary inline-block">
              View All Services
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            className="card p-12 bg-gradient-to-r from-pink-500 to-purple-600 text-white"
          >
            <h2 className="text-4xl font-playfair font-bold mb-4">
              Ready for a New Look?
            </h2>
            <p className="text-xl mb-8 opacity-90">
              Book your appointment today and get 20% off your first visit!
            </p>
            <Link to="/booking" className="bg-white text-pink-600 px-8 py-3 rounded-full font-bold hover:shadow-lg transition-all inline-block">
              Book Now
            </Link>
          </motion.div>
        </div>
      </section>
    </Layout>
  );
};

export default Home;