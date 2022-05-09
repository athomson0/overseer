const Card = ({children}) => {
    return (
        <div className="card w-80 bg-base-300 mx-6 my-3 shadow-lg hover:shadow-xl text-base hover:bg-base-200 transition-colors">
            {children}
        </div>
    )
}

export default Card;