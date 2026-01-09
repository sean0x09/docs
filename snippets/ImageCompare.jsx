import React, { useEffect, useState, useRef } from 'react';

/**
 * ImageCompare - A reusable image comparison slider component for Mintlify documentation
 * 
 * @param {string} beforeImage - URL of the "before" image
 * @param {string} afterImage - URL of the "after" image
 * @param {string} beforeLabel - Label for the "before" image (default: "Before")
 * @param {string} afterLabel - Label for the "after" image (default: "After")
 */
const ImageCompare = ({ 
  beforeImage, 
  afterImage, 
  beforeLabel = "Before", 
  afterLabel = "After" 
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [hasError, setHasError] = useState(false);
  const sliderRef = useRef(null);
  const scriptLoadedRef = useRef(false);

  useEffect(() => {
    // Check if we're in a browser environment
    if (typeof window === 'undefined' || typeof document === 'undefined') {
      return;
    }

    // Only load the script once
    if (scriptLoadedRef.current) {
      setIsLoaded(true);
      return;
    }

    // Check if the web component is already defined
    if (customElements && customElements.get('img-comparison-slider')) {
      scriptLoadedRef.current = true;
      setIsLoaded(true);
      return;
    }

    // Check if CSS is already loaded
    const existingLink = document.querySelector('link[href*="img-comparison-slider"]');
    if (!existingLink) {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = 'https://cdn.jsdelivr.net/npm/img-comparison-slider@8/dist/styles.css';
      document.head.appendChild(link);
    }

    // Check if custom styles are already added
    const existingStyle = document.getElementById('image-compare-custom-styles');
    if (!existingStyle) {
      const style = document.createElement('style');
      style.id = 'image-compare-custom-styles';
      style.textContent = `
        img-comparison-slider {
          --divider-width: 2px;
          --divider-color: rgba(0, 0, 0, 0.2);
          --default-handle-opacity: 1;
          --default-handle-width: 48px;
          --default-handle-color: #fff;
          --default-handle-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
          display: block;
          width: 100%;
          max-width: 100%;
          margin: 1.5rem 0;
          border-radius: 0.5rem;
          overflow: hidden;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
          border: 1px solid rgba(0, 0, 0, 0.1);
        }

        img-comparison-slider img {
          width: 100%;
          height: auto;
          display: block;
        }

        img-comparison-slider::part(handle) {
          background: var(--default-handle-color);
          box-shadow: var(--default-handle-shadow);
          border: 2px solid rgba(0, 0, 0, 0.1);
        }

        img-comparison-slider::part(divider) {
          background: var(--divider-color);
        }

        @media (prefers-color-scheme: dark) {
          img-comparison-slider {
            --divider-color: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.1);
          }

          img-comparison-slider::part(handle) {
            border-color: rgba(255, 255, 255, 0.2);
          }
        }

        @media (max-width: 768px) {
          img-comparison-slider {
            margin: 1rem 0;
            border-radius: 0.375rem;
          }
        }
      `;
      document.head.appendChild(style);
    }

    // Check if script is already loaded
    const existingScript = document.querySelector('script[src*="img-comparison-slider"]');
    if (existingScript) {
      // Script exists, wait for it to load
      if (customElements && customElements.get('img-comparison-slider')) {
        scriptLoadedRef.current = true;
        setIsLoaded(true);
      } else {
        existingScript.addEventListener('load', () => {
          scriptLoadedRef.current = true;
          setIsLoaded(true);
        });
      }
      return;
    }

    // Load the JavaScript
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/img-comparison-slider@8/dist/index.js';
    script.defer = true;
    script.onload = () => {
      scriptLoadedRef.current = true;
      setIsLoaded(true);
    };
    script.onerror = () => {
      setHasError(true);
    };
    document.body.appendChild(script);
  }, []);

  // Handle image loading errors
  const handleImageError = (imageType) => {
    console.error(`Failed to load ${imageType} image`);
    setHasError(true);
  };

  if (hasError) {
    return (
      <div style={{
        padding: '2rem',
        textAlign: 'center',
        backgroundColor: '#fef2f2',
        border: '1px solid #fecaca',
        borderRadius: '0.5rem',
        margin: '1.5rem 0',
        color: '#991b1b'
      }}>
        <p><strong>Error loading image comparison.</strong></p>
        <p style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>
          Please check that both image URLs are valid.
        </p>
      </div>
    );
  }

  if (!isLoaded) {
    return (
      <div style={{
        padding: '2rem',
        textAlign: 'center',
        backgroundColor: '#f9fafb',
        border: '1px solid #e5e7eb',
        borderRadius: '0.5rem',
        margin: '1.5rem 0'
      }}>
        <p style={{ color: '#6b7280' }}>Loading image comparison...</p>
      </div>
    );
  }

  return (
    <div style={{ position: 'relative', width: '100%' }}>
      <img-comparison-slider ref={sliderRef}>
        <img 
          slot="first" 
          src={beforeImage} 
          alt={beforeLabel}
          onError={() => handleImageError('before')}
          loading="lazy"
        />
        <img 
          slot="second" 
          src={afterImage} 
          alt={afterLabel}
          onError={() => handleImageError('after')}
          loading="lazy"
        />
        <div slot="handle" style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          width: '48px',
          height: '48px',
          borderRadius: '50%',
          backgroundColor: '#fff',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)',
          border: '2px solid rgba(0, 0, 0, 0.1)'
        }}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            width="24"
            height="24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            style={{ color: '#374151' }}
            aria-hidden="true"
          >
            <path d="M9 18l6-6-6-6" />
          </svg>
        </div>
      </img-comparison-slider>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        marginTop: '0.75rem',
        fontSize: '0.875rem',
        color: '#6b7280'
      }}>
        <span>{beforeLabel}</span>
        <span>{afterLabel}</span>
      </div>
    </div>
  );
};

export default ImageCompare;

