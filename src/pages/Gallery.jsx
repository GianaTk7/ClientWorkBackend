import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Layout from '../components/Layout';
import { XMarkIcon, HeartIcon, ShareIcon, ArrowLeftIcon, ArrowRightIcon } from '@heroicons/react/24/outline';
import { HeartIcon as HeartSolidIcon } from '@heroicons/react/24/solid';
import toast from 'react-hot-toast';

const Gallery = () => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedImage, setSelectedImage] = useState(null);
  const [likedImages, setLikedImages] = useState({});
  const [galleryImages, setGalleryImages] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
  
  // Fetch categories on mount
  useEffect(() => {
    fetchCategories();
  }, []);
  
  // Fetch images when category changes
  useEffect(() => {
    fetchImages();
  }, [selectedCategory]);
  
  const fetchCategories = async () => {
    try {
      const response = await fetch(`${API_URL}/api/gallery/categories`);
      if (!response.ok) throw new Error('Failed to fetch categories');
      const data = await response.json();
      setCategories(data);
    } catch (err) {
      console.error('Error fetching categories:', err);
      toast.error('Failed to load categories');
    }
  };
  
  const fetchImages = async () => {
    setLoading(true);
    setError(null);
    try {
      const url = selectedCategory === 'all' 
        ? `${API_URL}/api/gallery`
        : `${API_URL}/api/gallery?category=${selectedCategory}`;
      
      const response = await fetch(url);
      if (!response.ok) throw new Error('Failed to fetch images');
      const data = await response.json();
      setGalleryImages(data.images);
    } catch (err) {
      console.error('Error fetching images:', err);
      setError('Failed to load gallery images. Please try again later.');
      toast.error('Failed to load gallery images');
    } finally {
      setLoading(false);
    }
  };
  
const handleLike = async (imageId, e) => {
  if (e) e.stopPropagation();

  if (!imageId) return toast.error("Invalid image");

  if (likedImages[imageId]) return toast.info("You already liked this image!");

  try {
    const url = `${API_URL}/api/gallery/${imageId}/like`;
    const response = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' } });
    const result = await response.json().catch(() => ({}));

    if (!response.ok) throw new Error(result.detail || result.message || "Failed to like image");

    // Update grid
    setGalleryImages(prevImages =>
      prevImages.map(img =>
        img._id === imageId ? { ...img, likes: result.likes ?? (img.likes + 1) } : img
      )
    );

    // Update modal
    setSelectedImage(prev =>
      prev && prev._id === imageId ? { ...prev, likes: result.likes ?? (prev.likes + 1) } : prev
    );

    // Mark liked
    setLikedImages(prev => ({ ...prev, [imageId]: true }));

    toast.success("Thanks for liking!");
  } catch (err) {
    console.error("Error liking image:", err);
    toast.error(err.message || "Failed to like image");
  }
};
  
  const handleShare = async (image) => {
    const shareData = {
      title: image.title,
      text: image.description,
      url: `${window.location.origin}/gallery/${image._id}`
    };
    
    try {
      if (navigator.share) {
        await navigator.share(shareData);
      } else {
        await navigator.clipboard.writeText(shareData.url);
        toast.success('Link copied to clipboard!');
      }
    } catch (err) {
      console.error('Error sharing:', err);
    }
  };
  
  const nextImage = () => {
    const currentIndex = galleryImages.findIndex(img => img._id === selectedImage?._id);
    if (currentIndex < galleryImages.length - 1) {
      setSelectedImage(galleryImages[currentIndex + 1]);
    }
  };
  
  const prevImage = () => {
    const currentIndex = galleryImages.findIndex(img => img._id === selectedImage?._id);
    if (currentIndex > 0) {
      setSelectedImage(galleryImages[currentIndex - 1]);
    }
  };
  
const getCategoryInfo = (categoryName) => {
  
  const names = {
    'all': 'All Styles',
    'braids': 'Braids',
    'wigs': 'Wigs',
    'locs': 'Locs',
    'natural': 'Natural Hair'
  };
  
  return {
    name: names[categoryName] || categoryName
  };
};
  
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
  };
  
  return (
    <Layout>
      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-pink-600 to-purple-600 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-4xl md:text-5xl font-playfair font-bold text-white mb-4"
          >
            Our Work Gallery
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-xl text-white/90 max-w-2xl mx-auto"
          >
            Explore our latest transformations and get inspired for your next look
          </motion.p>
        </div>
      </section>
      
      {/* Category Filters */}
      <div className="sticky top-20 z-20 bg-white/95 backdrop-blur-md shadow-md py-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-wrap justify-center gap-3">
            {categories.map((category) => {
              const { icon, name } = getCategoryInfo(category.name);
              return (
                <button
                  key={category.name}
                  onClick={() => setSelectedCategory(category.name)}
                  className={`px-6 py-2 rounded-full font-semibold transition-all ${
                    selectedCategory === category.name
                      ? 'bg-gradient-to-r from-pink-500 to-purple-500 text-white shadow-lg'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  <span className="mr-2">{icon}</span>
                  {name} ({category.count})
                </button>
              );
            })}
          </div>
        </div>
      </div>
      
      {/* Gallery Grid */}
      <section className="py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {loading ? (
            <div className="flex justify-center items-center py-20">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-500"></div>
            </div>
          ) : error ? (
            <div className="text-center py-20">
              <p className="text-red-500 text-lg">{error}</p>
              <button
                onClick={fetchImages}
                className="mt-4 px-6 py-2 bg-pink-500 text-white rounded-lg hover:bg-pink-600"
              >
                Try Again
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {galleryImages.map((image, index) => (
                <motion.div
                  key={image._id}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.05 }}
                  className="group cursor-pointer"
                  onClick={() => setSelectedImage(image)}
                >
                  <div className="relative overflow-hidden rounded-2xl shadow-lg bg-white">
                    <div className="relative overflow-hidden aspect-square">
                      <img
                        src={image.image_url}
                        alt={image.title}
                        className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                        loading="lazy"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                      
                      <div className="absolute bottom-0 left-0 right-0 p-4 text-white transform translate-y-full group-hover:translate-y-0 transition-transform duration-300">
                        <h3 className="font-bold text-lg">{image.title}</h3>
                        <p className="text-sm text-white/80">{image.stylist_name}</p>
                      </div>
                    </div>
                    
                    <div className="p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="font-semibold text-gray-800">{image.title}</h3>
                          <p className="text-sm text-gray-500">{image.stylist_name}</p>
                        </div>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleLike(image._id);
                          }}
                          className="flex items-center gap-1 text-gray-500 hover:text-pink-500 transition-colors"
                          disabled={likedImages[image._id]}
                        >
                          {likedImages[image._id] ? (
                            <HeartSolidIcon className="w-5 h-5 text-pink-500" />
                          ) : (
                            <HeartIcon className="w-5 h-5" />
                          )}
                          <span className="text-sm">{image.likes}</span>
                        </button>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
          
          {!loading && !error && galleryImages.length === 0 && (
            <div className="text-center py-20">
              <p className="text-gray-500 text-lg">No images in this category yet.</p>
            </div>
          )}
        </div>
      </section>
      
      {/* Lightbox Modal */}
      <AnimatePresence>
        {selectedImage && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/95 flex items-center justify-center p-4"
            onClick={() => setSelectedImage(null)}
          >
            <button
              onClick={() => setSelectedImage(null)}
              className="absolute top-4 right-4 text-white hover:text-pink-500 transition-colors"
            >
              <XMarkIcon className="w-8 h-8" />
            </button>
            
            <button
              onClick={(e) => { e.stopPropagation(); prevImage(); }}
              className="absolute left-4 top-1/2 transform -translate-y-1/2 text-white hover:text-pink-500 transition-colors disabled:opacity-50"
              disabled={galleryImages.findIndex(img => img._id === selectedImage._id) === 0}
            >
              <ArrowLeftIcon className="w-8 h-8" />
            </button>
            
            <button
              onClick={(e) => { e.stopPropagation(); nextImage(); }}
              className="absolute right-4 top-1/2 transform -translate-y-1/2 text-white hover:text-pink-500 transition-colors disabled:opacity-50"
              disabled={galleryImages.findIndex(img => img._id === selectedImage._id) === galleryImages.length - 1}
            >
              <ArrowRightIcon className="w-8 h-8" />
            </button>
            
            <div 
              className="max-w-5xl max-h-[90vh] bg-white rounded-2xl overflow-hidden"
              onClick={(e) => e.stopPropagation()}
            >
              <img
                src={selectedImage.image_url}
                alt={selectedImage.title}
                className="w-full h-auto max-h-[70vh] object-contain"
              />
              <div className="p-6">
                <h3 className="text-2xl font-bold text-gray-800 mb-2">{selectedImage.title}</h3>
                <p className="text-gray-600 mb-4">{selectedImage.description}</p>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500">Stylist: {selectedImage.stylist_name}</p>
                    <p className="text-sm text-gray-500">Date: {formatDate(selectedImage.date_created)}</p>
                  </div>
                  <div className="flex gap-3">
                    <button
                      onClick={() => handleLike(selectedImage._id)}
                      className="flex items-center gap-2 px-4 py-2 rounded-full bg-gray-100 hover:bg-pink-100 transition-colors"
                    >
                      {likedImages[selectedImage._id] ? (
                        <HeartSolidIcon className="w-5 h-5 text-pink-500" />
                      ) : (
                        <HeartIcon className="w-5 h-5" />
                      )}
                      <span>{selectedImage.likes} Likes</span>
                    </button>
                    <button
                      onClick={() => handleShare(selectedImage)}
                      className="flex items-center gap-2 px-4 py-2 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors"
                    >
                      <ShareIcon className="w-5 h-5" />
                      <span>Share</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      
      {/* Call to Action */}
      <section className="py-16 bg-gradient-to-r from-pink-50 to-purple-50">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-playfair font-bold text-gray-800 mb-4">
            Ready to Transform Your Look?
          </h2>
          <p className="text-gray-600 mb-8">
            Book an appointment with our expert stylists and let us create your next masterpiece
          </p>
          <a
            href="/booking"
            className="inline-block bg-gradient-to-r from-pink-500 to-purple-500 text-white px-8 py-3 rounded-full font-semibold hover:shadow-lg transition-all"
          >
            Book Your Appointment
          </a>
        </div>
      </section>
    </Layout>
  );
};

export default Gallery;