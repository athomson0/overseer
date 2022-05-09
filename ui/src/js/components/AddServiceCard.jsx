import { useEffect, useState } from "react";
import Card from "./Card";

const AddServiceCard = ({addServiceFn}) => {
    const [open, setOpen] = useState(false);
    const toggle = () => setOpen(!open); 

    const addService = ((e) => {
        e.preventDefault();
        
        const serviceName = e.target.elements.serviceName.value;
        const connectionString = e.target.elements.connectionString.value;

        addServiceFn({name: serviceName, connectionString: connectionString});
        toggle();
    });

    if (!open) {
        return (
            <Card>
                <div className="card-body">
                    <h2 className="card-title justify-center text-success">Add a service</h2>
                    <p className="py-20 text-center">When you add a service, it will automatically be monitored for uptime.</p>
                    <div className="card-actions justify-center">
                        <button className="btn btn-success w-full bottom-0" onClick={toggle}>Add Service</button>
                    </div>
                </div>
            </Card>
        )
    }

    return (<Card>
                <div className="card-actions justify-end">
                        <button onClick={toggle} className="btn btn-square btn-sm">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" /></svg>
                        </button>
                </div>
                <h2 className="card-title justify-center text-success">Add a service</h2>
                <div className="card-body">
                    <form onSubmit={addService} className="form-control w-full max-w-xs">
                        <label className="label">
                            <span className="label-text">Service Name</span>
                        </label>
                        <input name="serviceName" type="text" placeholder="https://asdf.com" className="input input-sm input-bordered w-full max-w-xs" />

                        <label className="label">
                            <span className="label-text">Connection String</span>
                        </label>
                        <input name="connectionString" type="text" placeholder="mysql://127.0.0.1:3306" className="input input-sm input-bordered w-full max-w-xs" />
                        <button type="submit" className="btn btn-success w-full mt-24">Add Service</button>
                    </form>
                </div>
            </Card>
    )
}

export default AddServiceCard;