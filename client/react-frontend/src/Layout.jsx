import Header from './Header';
import Footer from './Footer';

function Layout({ children }) {
  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-b from-white to-red-500">
      {/* Common Header */}
      <div className="w-full max-w-5xl mx-auto">
      <div className="p-4 ">
      <Header />
      </div>

      {/* Page Content */}
     
      {/* Page Content */}
      <main className="flex p-4"> {/* Added flex and justify-center */}
        <div className="w-full"> {/* This div ensures a max width to center the content */}
          {children} {/* This is where the routed page content will go */}
        </div>
        </main>
        </div>
        <Footer />
    </div>
  );
}

export default Layout;