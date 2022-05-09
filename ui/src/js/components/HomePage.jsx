import { useEffect, useState } from 'react';
import ServiceCard from './ServiceCard';
import AddServiceCard from './AddServiceCard';
import apiClient from '../Api';

// const defaultServices = [
//     {
//         name: "Google", 
//         online: true, 
//         connection_string: "https://google.com", 
//         type: "Website", 
//         response_time: 762,
//         last_checker: 1651882002
//     },
//     {
//         name: "Reddit", 
//         online: false, 
//         connection_string: "https://reddit.com", 
//         type: "Website", 
//         response_time: 1262,
//         last_checker: 1651881002
//     },
//     {
//         name: "Local Database", 
//         online: "unknown", 
//         connection_string: "mysql://127.0.0.1:3306", 
//         type: "MySQL Database", 
//         response_time: null,
//         last_checker: 1651852003
//     },
// ];

const HomePage = () => {
    const [services, setServices] = useState([]);

    const addService = (service) => {
        service = {
            key: service.name,
            name: service.name, 
            online: true, 
            connectionString: service.connectionString, 
            type: "Website", 
            responseTime: 500
        };

        console.log(service);
        setServices([...services, service]);
    }

    const fetchAndSetServices = () => {
        apiClient.get("/services").then(res => {
            setServices(res.data.results);
        });
    }

    useEffect(() => {
        const timeout = setTimeout(() => {
            fetchAndSetServices();
        }, 2500);
      
        return () => clearTimeout(timeout);
    }, [services]);

    const removeService = (service) => {
        setServices(services.filter(existingService => {
            return service.name !== existingService.name;
        }));
    }

    return (
        <div>
            <div className="flex flex-row flex-wrap justify-center py-24">
                {services.map((service) => {
                    return <ServiceCard key={service.id} service={service} removeServiceFn={removeService} />
                })}
                
                <AddServiceCard addServiceFn={addService} />
            </div>   
        </div>
    )
}

export default HomePage;