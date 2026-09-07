import { useEffect, useState } from 'react'
import Header from './components/layout/Header'
import Hero from './components/layout/Hero'
import TripForm from './components/trip/TripForm'
import TripList from './components/trip/TripList'
import TripDetail from './components/trip/TripDetail'
import DestinationSearch from './components/destination/DestinationSearch'
import { request } from './services/api'

const emptyForm = { title: '', destination_id: '', start_date: '', end_date: '', budget: 2500, travelers: 2, interests: '', travel_style: 'balanced' }

export default function App() {
  const [destinations, setDestinations] = useState([]); const [trips, setTrips] = useState([]); const [form, setForm] = useState(emptyForm); const [selectedTrip, setSelectedTrip] = useState(null); const [expense, setExpense] = useState({ category: 'food', description: '', estimated_amount: '' }); const [loading, setLoading] = useState(true); const [message, setMessage] = useState('')
  const refresh = async () => { const [destinationData, tripData] = await Promise.all([request('/api/v1/destinations'), request('/api/v1/trips')]); setDestinations(destinationData); setTrips(tripData); if (selectedTrip) setSelectedTrip(tripData.find((trip) => trip.id === selectedTrip.id) || null) }
  useEffect(() => { refresh().catch((error) => setMessage(error.message)).finally(() => setLoading(false)) }, [])
  const createTrip = async (event) => { event.preventDefault(); try { const trip = await request('/api/v1/trips', { method: 'POST', body: JSON.stringify({ ...form, destination_id: Number(form.destination_id), budget: Number(form.budget), travelers: Number(form.travelers) }) }); setForm(emptyForm); setSelectedTrip(trip); setMessage('Trip created. Generate an itinerary when you are ready.'); await refresh() } catch (error) { setMessage(error.message) } }
  const generate = async () => { try { const trip = await request(`/api/v1/trips/${selectedTrip.id}/generate`, { method: 'POST' }); setSelectedTrip(trip); await refresh(); setMessage('Your day-by-day plan is ready.') } catch (error) { setMessage(error.message) } }
  const addExpense = async (event) => { event.preventDefault(); try { const trip = await request(`/api/v1/trips/${selectedTrip.id}/expenses`, { method: 'POST', body: JSON.stringify({ ...expense, estimated_amount: Number(expense.estimated_amount) }) }); setSelectedTrip(trip); setExpense({ category: 'food', description: '', estimated_amount: '' }); await refresh(); setMessage('Expense added to your trip budget.') } catch (error) { setMessage(error.message) } }
  if (loading) return <div className="loading">Loading your travel workspace...</div>
  return <main className="app-shell"><Header /><Hero tripCount={trips.length} />{message && <div className="notice">{message}</div>}<div className="workspace"><TripForm form={form} setForm={setForm} destinations={destinations} onSubmit={createTrip} /><DestinationSearch destinations={destinations} form={form} setForm={setForm} setDestinations={setDestinations} setMessage={setMessage} /></div><TripList trips={trips} selectedTrip={selectedTrip} onSelect={setSelectedTrip} />{selectedTrip && <TripDetail trip={selectedTrip} onGenerate={generate} expense={expense} setExpense={setExpense} onAddExpense={addExpense} />}</main>
}
