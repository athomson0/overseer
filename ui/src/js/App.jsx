import HomePage from './components/HomePage';
import Header from './components/Header';
import Footer from './components/Footer';
import '../css/App.css';

const Overseer = () => {
    return (
        <div className="min-h-screen sm:h-max 2xl:h-screen bg-gradient-to-t from-slate-900 to-slate-700">
            <div className="container mx-auto h-full">
                <Header />
                <div className="flex items-center justify-center">
                    <HomePage />
                </div>
                <Footer />
            </div>
        </div>
    )
}

export default Overseer;