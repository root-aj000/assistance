'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const NavBar = () => {
  const pathname = usePathname();

  const navItems = [
    { name: 'Home', path: '/', icon: '🏠' },
    { name: 'Chat', path: '/chat', icon: '💬' },
    { name: 'Index', path: '/index', icon: '📚' },
    { name: 'Settings', path: '/settings', icon: '⚙️' },
    { name: 'About', path: '/about', icon: 'ℹ️' },
  ];

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo/Brand */}
          <div className="flex items-center space-x-2">
            <span className="text-2xl">🧠</span>
            <h1 className="text-xl font-bold text-gray-900">
              Vibe Coding AI
            </h1>
          </div>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const isActive = pathname === item.path;
              return (
                <Link
                  key={item.path}
                  href={item.path}
                  className={`
                    px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200
                    flex items-center space-x-2
                    ${
                      isActive
                        ? 'bg-indigo-600 text-white shadow-md'
                        : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
                    }
                  `}
                >
                  <span>{item.icon}</span>
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </div>

          {/* API Docs Link */}
          <div className="flex items-center space-x-4">
            <a
              href="http://localhost:5001/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
            >
              📖 API Docs
            </a>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden pb-3 pt-2">
          <div className="flex overflow-x-auto space-x-2 no-scrollbar">
            {navItems.map((item) => {
              const isActive = pathname === item.path;
              return (
                <Link
                  key={item.path}
                  href={item.path}
                  className={`
                    px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap
                    flex items-center space-x-1.5 transition-all duration-200
                    ${
                      isActive
                        ? 'bg-indigo-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }
                  `}
                >
                  <span>{item.icon}</span>
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default NavBar;
