import Card from "./Card";

import { timeSince } from "../Util";

const ServiceCard = ({service, removeServiceFn}) => {
    let {name, connection_string, online, stype, response_time, last_checked} = service;
    
    console.log(name, connection_string)

    const headerImage = "https://api.lorem.space/image/shoes?w=600&h=400";

    // TODO
    const trimconnection_string = (connection_string) => {
        return connection_string;
    }

    const removeService = () => {
        removeServiceFn(service);
    }

    return (
        <Card>
            <div className="card-actions justify-end">
                    <button onClick={removeService} className="btn btn-square btn-sm absolute bg-transparent border-r-0 border-none hover:bg-transparent">
                <div className="tooltip tooltip-left normal-case" data-tip="Delete this service">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-secondary-focus hover:text-secondary-content" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" /></svg>
                </div>
                    </button>
                <figure className=""><img src={headerImage} alt="Shoes" /></figure>
            </div>
            <div className="card-body">
                <h2 className="card-title hover:cursor-default">
                    {name}
                    <div className="tooltip tooltip-right" data-tip={online == true && "Online" || (online == "unknown" ? "Unknown" : "Offline")}>
                        <span className={`mx-1 mt-2 badge badge-${online ? "success" : "error"}`}></span>
                    </div>
                </h2>
                <div className="my-3 flex-grow border-t border-base-100"></div>
                <a href="#" className="py-2 text-neutral-content hover:text-primary-content">{trimconnection_string(connection_string)}</a>
            
                <div className="card-actions justify-start mt-2">
                    <div className="flex flex-row p-3 font-bold hover:cursor-default badge badge-info">{stype}</div> 
                    {(online == true && last_checked && response_time !== 0) &&
                        <div className={`flex-flex-row p-3 hover:cursor-default font-bold badge badge-${response_time < 1000 ? "success" : "warning"}`}>{response_time}ms</div>}
                    {last_checked && 
                        <div className="tooltip" data-tip={`Last checked ${timeSince(last_checked, false)}`}>
                            <div className="p-3 font-bold hover:cursor-default badge">{timeSince(last_checked)}</div> 
                        </div>}
                </div>
            </div>
        </Card>
    )
}

export default ServiceCard;