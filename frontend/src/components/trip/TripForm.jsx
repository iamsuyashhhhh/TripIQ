export default function TripForm({ form, setForm, destinations, onSubmit }) {
  const update = (key) => (event) => setForm({ ...form, [key]: event.target.value })
  return (
    <section className="panel planner">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">01 / START PLANNING</p>
          <h2>Build a new trip</h2>
        </div>
        <span className="step">2 min setup</span>
      </div>
      <form onSubmit={onSubmit} className="trip-form">
        <label>
          Trip name
          <input
            required
            placeholder="Summer in Japan"
            value={form.title}
            onChange={update('title')}
          />
        </label>
        <label>
          Destination
          <select required value={form.destination_id} onChange={update('destination_id')}>
            <option value="">Choose a place</option>
            {destinations.map((destination) => (
              <option key={destination.id} value={destination.id}>
                {destination.name}, {destination.country}
              </option>
            ))}
          </select>
        </label>
        <div className="form-row">
          <label>
            Start date
            <input required type="date" value={form.start_date} onChange={update('start_date')} />
          </label>
          <label>
            End date
            <input required type="date" value={form.end_date} onChange={update('end_date')} />
          </label>
        </div>
        <div className="form-row">
          <label>
            Budget (USD)
            <input required type="number" min="1" value={form.budget} onChange={update('budget')} />
          </label>
          <label>
            Travelers
            <input
              required
              type="number"
              min="1"
              max="20"
              value={form.travelers}
              onChange={update('travelers')}
            />
          </label>
        </div>
        <label>
          What are you into?
          <input
            placeholder="Food, design, hiking..."
            value={form.interests}
            onChange={update('interests')}
          />
        </label>
        <label>
          Travel style
          <select value={form.travel_style} onChange={update('travel_style')}>
            <option value="balanced">Balanced</option>
            <option value="slow">Slow and local</option>
            <option value="packed">Packed with highlights</option>
            <option value="luxury">Comfort first</option>
          </select>
        </label>
        <button className="primary" type="submit">
          Create trip <span>↗</span>
        </button>
      </form>
    </section>
  )
}
