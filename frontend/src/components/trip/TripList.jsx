export default function TripList({ trips, selectedTrip, onSelect }) {
  return (
    <section className="panel trips-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">03 / YOUR JOURNEYS</p>
          <h2>Trips in motion</h2>
        </div>
      </div>
      {trips.length === 0 ? (
        <div className="empty">Your first trip is one good idea away.</div>
      ) : (
        <div className="trip-list">
          {trips.map((trip) => (
            <button
              className={`trip-row ${selectedTrip?.id === trip.id ? 'selected' : ''}`}
              key={trip.id}
              onClick={() => onSelect(trip)}
            >
              <span className="trip-number">0{trip.id}</span>
              <span className="trip-name">
                <strong>{trip.title}</strong>
                <small>
                  {trip.destination}, {trip.country} · {trip.start_date}
                </small>
              </span>
              <span className="trip-status">{trip.status}</span>
              <span>→</span>
            </button>
          ))}
        </div>
      )}
    </section>
  )
}
