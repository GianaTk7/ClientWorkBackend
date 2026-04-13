import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { UserIcon, EnvelopeIcon, PhoneIcon, CalendarIcon, ClockIcon, ScissorsIcon, UserGroupIcon, ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

const Booking = () => {
  const [loading, setLoading] = useState(false);
  const [services, setServices] = useState([]);
  const [stylists, setStylists] = useState([]);
  const [availableSlots, setAvailableSlots] = useState([]);
  const [loadingData, setLoadingData] = useState(true);
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    service_id: '',
    stylist_id: '',
    date: '',
    time: '',
    notes: ''
  });

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // Fetch services and stylists from backend
  useEffect(() => {
    fetchServices();
    fetchStylists();
  }, []);

  const fetchServices = async () => {
    try {
      const response = await fetch(`${API_URL}/api/services`);
      if (!response.ok) throw new Error('Failed to fetch services');
      const data = await response.json();
      setServices(data);
    } catch (err) {
      console.error('Error fetching services:', err);
      toast.error('Failed to load services');
    }
  };

  const fetchStylists = async () => {
    try {
      const response = await fetch(`${API_URL}/api/stylists`);
      if (!response.ok) throw new Error('Failed to fetch stylists');
      const data = await response.json();
      setStylists(data);
      setLoadingData(false);
    } catch (err) {
      console.error('Error fetching stylists:', err);
      toast.error('Failed to load stylists');
      setLoadingData(false);
    }
  };

  const fetchAvailability = async (stylistId, date) => {
    if (!stylistId || !date) return;
    
    try {
      const response = await fetch(`${API_URL}/api/stylists/${stylistId}/availability?date=${date}`);
      if (!response.ok) throw new Error('Failed to fetch availability');
      const data = await response.json();
      setAvailableSlots(data.available_slots);
    } catch (err) {
      console.error('Error fetching availability:', err);
      setAvailableSlots([]);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Fetch availability when stylist or date changes
    if (name === 'stylist_id' && formData.date) {
      fetchAvailability(value, formData.date);
    }
    if (name === 'date' && formData.stylist_id) {
      fetchAvailability(formData.stylist_id, value);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate required fields
    if (!formData.name || !formData.email || !formData.phone || !formData.service_id || !formData.stylist_id || !formData.date || !formData.time) {
      toast.error('Please fill in all required fields');
      return;
    }

    setLoading(true);
    
    try {
      const response = await fetch(`${API_URL}/api/book-appointment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          customer_name: formData.name,
          customer_email: formData.email,
          customer_phone: formData.phone,
          stylist_id: formData.stylist_id,
          service_id: formData.service_id,
          appointment_date: formData.date,
          appointment_time: formData.time,
          notes: formData.notes
        })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        toast.success('Appointment booked successfully!');
        console.log('Booking saved:', data);
        
        // Reset form
        setFormData({
          name: '', email: '', phone: '', service_id: '', stylist_id: '', date: '', time: '', notes: ''
        });
        setAvailableSlots([]);
      } else {
        throw new Error(data.detail || 'Booking failed');
      }
      
    } catch (error) {
      console.error('Booking error:', error);
      toast.error(error.message || 'Failed to book appointment. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loadingData) {
    return (
      <Layout>
        <div className="flex justify-center items-center h-screen">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-500"></div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-b from-pink-50 to-purple-50 py-12">
        <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-3xl md:text-4xl font-playfair font-bold text-gray-800 mb-2">
              Book Your Appointment
            </h1>
            <p className="text-gray-600">Fill out the form below to schedule your service</p>
          </div>

          {/* Booking Form */}
          <div className="bg-white rounded-2xl shadow-xl p-6 md:p-8">
            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Name */}
              <div>
                <label className="block text-gray-700 font-semibold mb-2">
                  <UserIcon className="w-4 h-4 inline mr-2 text-pink-500" />
                  Full Name *
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                  placeholder="Enter your full name"
                />
              </div>

              {/* Email */}
              <div>
                <label className="block text-gray-700 font-semibold mb-2">
                  <EnvelopeIcon className="w-4 h-4 inline mr-2 text-pink-500" />
                  Email Address *
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                  placeholder="you@example.com"
                />
              </div>

              {/* Phone */}
              <div>
                <label className="block text-gray-700 font-semibold mb-2">
                  <PhoneIcon className="w-4 h-4 inline mr-2 text-pink-500" />
                  Phone Number *
                </label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                  placeholder="(123) 456-7890"
                />
              </div>

              {/* Service */}
              <div>
                <label className="block text-gray-700 font-semibold mb-2">
                  <ScissorsIcon className="w-4 h-4 inline mr-2 text-pink-500" />
                  Select Service *
                </label>
                <select
                  name="service_id"
                  value={formData.service_id}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                >
                  <option value="">Choose a service</option>
                  {services.map((service) => (
                    <option key={service._id} value={service._id}>
                      {service.name} - ${service.price}
                    </option>
                  ))}
                </select>
              </div>
              {/* Date and Time */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-gray-700 font-semibold mb-2">
                    <CalendarIcon className="w-4 h-4 inline mr-2 text-pink-500" />
                    Date *
                  </label>
                  <input
                    type="date"
                    name="date"
                    value={formData.date}
                    onChange={handleChange}
                    required
                    min={new Date().toISOString().split('T')[0]}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-gray-700 font-semibold mb-2">
                    <ClockIcon className="w-4 h-4 inline mr-2 text-pink-500" />
                    Time *
                  </label>
                  <select
                    name="time"
                    value={formData.time}
                    onChange={handleChange}
                    required
                    disabled={!formData.stylist_id || !formData.date}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent disabled:bg-gray-100"
                  >
                    <option value="">Select time</option>
                    {availableSlots.map((slot, index) => (
                      <option key={index} value={slot}>{slot}</option>
                    ))}
                  </select>
                  {(!formData.stylist_id || !formData.date) && (
                    <p className="text-xs text-gray-500 mt-1">Select stylist and date first</p>
                  )}
                </div>
              </div>

              {/* Notes */}
              <div>
                <label className="block text-gray-700 font-semibold mb-2">
                  <ChatBubbleLeftRightIcon className="w-4 h-4 inline mr-2 text-pink-500" />
                  Special Requests (Optional)
                </label>
                <textarea
                  name="notes"
                  value={formData.notes}
                  onChange={handleChange}
                  rows="3"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                  placeholder="Any special requests or notes for your stylist..."
                />
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-pink-500 to-purple-500 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 mt-6"
              >
                {loading ? 'Booking...' : 'Book Appointment'}
              </button>
            </form>

            <p className="text-center text-sm text-gray-500 mt-6">
              A confirmation will be sent to your email after booking
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Booking;