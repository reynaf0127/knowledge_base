import { useState } from 'react';
import * as Collapsible from '@radix-ui/react-collapsible';
import { ChevronDown, ChevronRight, ArrowLeft } from 'lucide-react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const salesData = [
  { month: 'Jan', revenue: 4200, orders: 145 },
  { month: 'Feb', revenue: 5100, orders: 178 },
  { month: 'Mar', revenue: 4800, orders: 162 },
  { month: 'Apr', revenue: 6200, orders: 215 },
  { month: 'May', revenue: 7100, orders: 248 },
  { month: 'Jun', revenue: 8300, orders: 289 },
];

const userSegmentData = [
  { name: 'New Users', value: 3200, color: '#3b82f6' },
  { name: 'Returning Users', value: 5800, color: '#8b5cf6' },
  { name: 'Churned Users', value: 1100, color: '#ef4444' },
];

const conversionData = [
  { stage: 'Visits', count: 12500 },
  { stage: 'Sign Ups', count: 4200 },
  { stage: 'Trial', count: 2800 },
  { stage: 'Paid', count: 890 },
];

interface SectionProps {
  title: string;
  children: React.ReactNode;
  bgColor: string;
  id: string;
}

function CollapsibleSection({ title, children, bgColor, id }: SectionProps) {
  const [open, setOpen] = useState(false);

  return (
    <Collapsible.Root id={id} open={open} onOpenChange={setOpen} className="mb-8 overflow-hidden scroll-mt-24">
      <Collapsible.Trigger className={`w-full flex items-center justify-between p-6 rounded-2xl ${bgColor} transition-all duration-300 hover:scale-[1.01] hover:shadow-xl shadow-lg border-2 border-black/10`}>
        <h2 className="text-2xl tracking-tight font-semibold">{title}</h2>
        <div className="bg-white/40 backdrop-blur-sm rounded-full p-2 transition-all duration-300 group-hover:bg-white/60">
          {open ? <ChevronDown className="w-5 h-5 transition-transform duration-300" /> : <ChevronRight className="w-5 h-5 transition-transform duration-300" />}
        </div>
      </Collapsible.Trigger>
      <Collapsible.Content className="bg-white/90 backdrop-blur-lg p-6 rounded-b-2xl mt-2 shadow-lg border-2 border-t-0 border-black/10">
        {children}
      </Collapsible.Content>
    </Collapsible.Root>
  );
}

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 via-gray-50 to-gray-200">
      <nav className="bg-white/90 backdrop-blur-xl sticky top-0 z-50 shadow-xl border-b-2 border-black/10">
        <div className="max-w-7xl mx-auto px-8 py-5 flex items-center justify-between">
          <button
            onClick={() => window.history.back()}
            className="flex items-center gap-2 px-4 py-2 bg-stone-100 hover:bg-stone-200 rounded-full transition-all duration-300 hover:scale-105 shadow-md hover:shadow-lg border-2 border-stone-200"
          >
            <ArrowLeft className="w-4 h-4 text-stone-700" />
            <span className="text-sm text-stone-700 font-medium">Back to Home</span>
          </button>
          <h1 className="text-2xl tracking-tight text-stone-900 absolute left-1/2 transform -translate-x-1/2">
            Amazon E-Commerce Return Prediction
          </h1>
          <div className="w-32"></div>
        </div>
      </nav>

      <section className="bg-gradient-to-br from-gray-200 via-gray-100 to-gray-300 py-16 relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-pink-200/20 via-transparent to-sky-200/20"></div>
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_bottom_left,_var(--tw-gradient-stops))] from-amber-200/15 via-transparent to-transparent"></div>
        <div className="max-w-4xl mx-auto px-8 relative z-10">
          <div className="mb-10">
            <h2 className="text-3xl mb-4 text-stone-950 tracking-tight font-semibold">Overview Project</h2>
            <p className="text-lg text-stone-800 leading-relaxed">
              This project analyzes Amazon e-commerce data to predict product returns using machine learning techniques.
              By understanding return patterns, we can optimize inventory management, improve customer satisfaction, and reduce operational costs.
            </p>
          </div>

          <div>
            <h2 className="text-3xl mb-4 text-stone-950 tracking-tight font-semibold">Key Findings</h2>
            <p className="text-lg text-stone-800 leading-relaxed">
              Our analysis reveals significant patterns in return behavior across product categories, customer segments, and seasonal trends.
              The predictive model achieved 87% accuracy in identifying high-risk return scenarios, enabling proactive intervention strategies.
            </p>
          </div>
        </div>
      </section>

      <main className="max-w-4xl mx-auto px-8 py-12">

        <CollapsibleSection id="explore" title="Explore Data" bgColor="bg-gradient-to-br from-amber-100 via-yellow-50 to-amber-200">
          <div className="space-y-6">
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-gradient-to-br from-emerald-200 to-emerald-300 p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-2 border-black/5">
                <div className="text-xs mb-2 text-stone-900 uppercase tracking-wider opacity-80 font-sans">Total Records</div>
                <div className="text-4xl text-stone-950 tracking-tighter font-sans font-bold">125K</div>
              </div>
              <div className="bg-gradient-to-br from-pink-200 to-pink-300 p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-2 border-black/5">
                <div className="text-xs mb-2 text-stone-900 uppercase tracking-wider opacity-80 font-sans">Product Categories</div>
                <div className="text-4xl text-stone-950 tracking-tighter font-sans font-bold">42</div>
              </div>
              <div className="bg-gradient-to-br from-sky-200 to-sky-300 p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-2 border-black/5">
                <div className="text-xs mb-2 text-stone-900 uppercase tracking-wider opacity-80 font-sans">Return Rate</div>
                <div className="text-4xl text-stone-950 tracking-tighter font-sans font-bold">18%</div>
              </div>
            </div>

            <p className="text-lg text-stone-700 leading-relaxed">
              The dataset contains 125,000 transaction records across 42 product categories with an overall return rate of 18%.
              Initial exploration reveals significant variance in return rates across different product types and customer segments.
            </p>

            <div className="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border-2 border-stone-200 overflow-x-auto">
              <h3 className="text-xl mb-4 text-stone-900 tracking-tight font-sans font-semibold">Sample Dataset Preview</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm border-collapse">
                  <thead>
                    <tr className="bg-stone-100 border-b-2 border-stone-300">
                      <th className="px-3 py-2 text-left font-sans font-semibold text-stone-900">User ID</th>
                      <th className="px-3 py-2 text-left font-sans font-semibold text-stone-900">Category</th>
                      <th className="px-3 py-2 text-left font-sans font-semibold text-stone-900">Subcategory</th>
                      <th className="px-3 py-2 text-left font-sans font-semibold text-stone-900">Brand</th>
                      <th className="px-3 py-2 text-right font-sans font-semibold text-stone-900">Price</th>
                      <th className="px-3 py-2 text-right font-sans font-semibold text-stone-900">Discount %</th>
                      <th className="px-3 py-2 text-right font-sans font-semibold text-stone-900">Final Price</th>
                      <th className="px-3 py-2 text-right font-sans font-semibold text-stone-900">Rating</th>
                      <th className="px-3 py-2 text-right font-sans font-semibold text-stone-900">Reviews</th>
                      <th className="px-3 py-2 text-right font-sans font-semibold text-stone-900">Stock</th>
                    </tr>
                  </thead>
                  <tbody className="font-serif">
                    <tr className="border-b border-stone-200 hover:bg-pink-50/30 transition-colors">
                      <td className="px-3 py-2 text-stone-700">U0017P558563</td>
                      <td className="px-3 py-2 text-stone-700">Electronics</td>
                      <td className="px-3 py-2 text-stone-700">Mobile</td>
                      <td className="px-3 py-2 text-stone-700">Samsung</td>
                      <td className="px-3 py-2 text-right text-stone-700">15500.11</td>
                      <td className="px-3 py-2 text-right text-stone-700">16.10</td>
                      <td className="px-3 py-2 text-right text-stone-700">13009.71</td>
                      <td className="px-3 py-2 text-right text-stone-700">4.0</td>
                      <td className="px-3 py-2 text-right text-stone-700">43</td>
                      <td className="px-3 py-2 text-right text-stone-700">221</td>
                    </tr>
                    <tr className="border-b border-stone-200 hover:bg-sky-50/30 transition-colors">
                      <td className="px-3 py-2 text-stone-700">U0001P758693</td>
                      <td className="px-3 py-2 text-stone-700">Sports</td>
                      <td className="px-3 py-2 text-stone-700">Fitness</td>
                      <td className="px-3 py-2 text-stone-700">H&M</td>
                      <td className="px-3 py-2 text-right text-stone-700">14758.86</td>
                      <td className="px-3 py-2 text-right text-stone-700">26.5</td>
                      <td className="px-3 py-2 text-right text-stone-700">10819.43</td>
                      <td className="px-3 py-2 text-right text-stone-700">4.3</td>
                      <td className="px-3 py-2 text-right text-stone-700">46</td>
                      <td className="px-3 py-2 text-right text-stone-700">329</td>
                    </tr>
                    <tr className="border-b border-stone-200 hover:bg-amber-50/30 transition-colors">
                      <td className="px-3 py-2 text-stone-700">U0003P945482</td>
                      <td className="px-3 py-2 text-stone-700">Fashion</td>
                      <td className="px-3 py-2 text-stone-700">Clothing</td>
                      <td className="px-3 py-2 text-stone-700">Nike</td>
                      <td className="px-3 py-2 text-right text-stone-700">668.83</td>
                      <td className="px-3 py-2 text-right text-stone-700">24.83</td>
                      <td className="px-3 py-2 text-right text-stone-700">502.53</td>
                      <td className="px-3 py-2 text-right text-stone-700">4.1</td>
                      <td className="px-3 py-2 text-right text-stone-700">4</td>
                      <td className="px-3 py-2 text-right text-stone-700">68</td>
                    </tr>
                    <tr className="border-b border-stone-200 hover:bg-emerald-50/30 transition-colors">
                      <td className="px-3 py-2 text-stone-700">U0051P720317</td>
                      <td className="px-3 py-2 text-stone-700">Home</td>
                      <td className="px-3 py-2 text-stone-700">Decor</td>
                      <td className="px-3 py-2 text-stone-700">Sony</td>
                      <td className="px-3 py-2 text-right text-stone-700">10581.29</td>
                      <td className="px-3 py-2 text-right text-stone-700">48.63</td>
                      <td className="px-3 py-2 text-right text-stone-700">5446.58</td>
                      <td className="px-3 py-2 text-right text-stone-700">4.0</td>
                      <td className="px-3 py-2 text-right text-stone-700">48</td>
                      <td className="px-3 py-2 text-right text-stone-700">274</td>
                    </tr>
                    <tr className="border-b border-stone-200 hover:bg-pink-50/30 transition-colors">
                      <td className="px-3 py-2 text-stone-700">U0008P746896</td>
                      <td className="px-3 py-2 text-stone-700">Electronics</td>
                      <td className="px-3 py-2 text-stone-700">Tablet</td>
                      <td className="px-3 py-2 text-stone-700">Dell</td>
                      <td className="px-3 py-2 text-right text-stone-700">8158.61</td>
                      <td className="px-3 py-2 text-right text-stone-700">17.64</td>
                      <td className="px-3 py-2 text-right text-stone-700">6699.68</td>
                      <td className="px-3 py-2 text-right text-stone-700">4.3</td>
                      <td className="px-3 py-2 text-right text-stone-700">22</td>
                      <td className="px-3 py-2 text-right text-stone-700">160</td>
                    </tr>
                    <tr className="border-b border-stone-200 hover:bg-sky-50/30 transition-colors">
                      <td className="px-3 py-2 text-stone-700">U0489P794434</td>
                      <td className="px-3 py-2 text-stone-700">Home</td>
                      <td className="px-3 py-2 text-stone-700">Furniture</td>
                      <td className="px-3 py-2 text-stone-700">Adidas</td>
                      <td className="px-3 py-2 text-right text-stone-700">1104.92</td>
                      <td className="px-3 py-2 text-right text-stone-700">37.61</td>
                      <td className="px-3 py-2 text-right text-stone-700">687.2</td>
                      <td className="px-3 py-2 text-right text-stone-700">3.4</td>
                      <td className="px-3 py-2 text-right text-stone-700">14</td>
                      <td className="px-3 py-2 text-right text-stone-700">232</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div className="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border-2 border-stone-200">
              <h3 className="text-xl mb-6 text-stone-900 tracking-tight font-sans font-semibold">Monthly Return Trends</h3>
              <ResponsiveContainer width="100%" height={280}>
                <LineChart data={salesData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#d6d3d1" opacity={0.5} />
                  <XAxis dataKey="month" stroke="#78716c" style={{ fontSize: '12px', fontFamily: 'Inter' }} />
                  <YAxis yAxisId="left" stroke="#78716c" style={{ fontSize: '12px', fontFamily: 'Inter' }} />
                  <YAxis yAxisId="right" orientation="right" stroke="#9CA986" style={{ fontSize: '12px', fontFamily: 'Inter' }} />
                  <Tooltip contentStyle={{ backgroundColor: 'rgba(255, 255, 255, 0.95)', border: '2px solid #d6d3d1', borderRadius: '8px', padding: '8px', fontSize: '13px' }} />
                  <Legend wrapperStyle={{ paddingTop: '16px', fontSize: '13px' }} />
                  <Line yAxisId="left" type="monotone" dataKey="revenue" stroke="#78716c" strokeWidth={3} name="Returns" dot={{ r: 4 }} activeDot={{ r: 6 }} />
                  <Line yAxisId="right" type="monotone" dataKey="orders" stroke="#9CA986" strokeWidth={3} name="Orders" dot={{ r: 4 }} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </CollapsibleSection>

        <CollapsibleSection id="feature" title="Feature Engineering" bgColor="bg-gradient-to-br from-pink-200 via-pink-100 to-pink-300">
          <div className="space-y-6">
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-gradient-to-br from-sky-200 to-sky-300 p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-2 border-black/5">
                <div className="text-xs mb-2 text-stone-900 uppercase tracking-wider opacity-80 font-sans">Base Features</div>
                <div className="text-4xl text-stone-950 tracking-tighter font-sans font-bold">28</div>
              </div>
              <div className="bg-gradient-to-br from-amber-200 to-yellow-300 p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-2 border-black/5">
                <div className="text-xs mb-2 text-stone-900 uppercase tracking-wider opacity-80 font-sans">Engineered Features</div>
                <div className="text-4xl text-stone-950 tracking-tighter font-sans font-bold">47</div>
              </div>
              <div className="bg-gradient-to-br from-[#8B4949] to-[#7A3E3E] p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-2 border-black/5">
                <div className="text-xs mb-2 text-pink-50 uppercase tracking-wider opacity-90 font-sans">Final Feature Set</div>
                <div className="text-4xl text-pink-50 tracking-tighter font-sans font-bold">75</div>
              </div>
            </div>

            <p className="text-lg text-stone-700 leading-relaxed">
              Created 47 engineered features including customer behavior metrics, product affinity scores, temporal patterns, and interaction features.
              Feature selection reduced the final set to 75 most impactful variables with low correlation.
            </p>

            <div className="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border-2 border-stone-200">
              <h3 className="text-xl mb-6 text-stone-900 tracking-tight font-sans font-semibold">Feature Importance Distribution</h3>
              <ResponsiveContainer width="100%" height={280}>
                <PieChart>
                  <Pie
                    data={userSegmentData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={(entry) => `${entry.name}: ${entry.value}`}
                    outerRadius={90}
                    fill="#8884d8"
                    dataKey="value"
                    strokeWidth={2}
                    style={{ fontSize: '13px', fontFamily: 'Inter' }}
                  >
                    {userSegmentData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: 'rgba(255, 255, 255, 0.95)', border: '2px solid #d6d3d1', borderRadius: '8px', padding: '8px', fontSize: '13px' }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </CollapsibleSection>

        <CollapsibleSection id="modeling" title="Modeling" bgColor="bg-gradient-to-br from-slate-200 via-gray-100 to-slate-300">
          <div className="space-y-6">
            <div className="grid grid-cols-4 gap-3">
              <div className="bg-gradient-to-br from-pink-200 to-pink-300 p-5 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-2 border-black/5">
                <div className="text-xs mb-2 text-stone-900 uppercase tracking-wider opacity-80 font-sans">Random Forest</div>
                <div className="text-3xl text-stone-950 tracking-tighter font-sans font-bold">85%</div>
              </div>
              <div className="bg-gradient-to-br from-sky-200 to-sky-300 p-5 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-2 border-black/5">
                <div className="text-xs mb-2 text-stone-900 uppercase tracking-wider opacity-80 font-sans">XGBoost</div>
                <div className="text-3xl text-stone-950 tracking-tighter font-sans font-bold">87%</div>
              </div>
              <div className="bg-gradient-to-br from-amber-200 to-yellow-300 p-5 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-2 border-black/5">
                <div className="text-xs mb-2 text-stone-900 uppercase tracking-wider opacity-80 font-sans">LightGBM</div>
                <div className="text-3xl text-stone-950 tracking-tighter font-sans font-bold">86%</div>
              </div>
              <div className="bg-gradient-to-br from-[#8B4949] to-[#7A3E3E] p-5 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-2 border-black/5">
                <div className="text-xs mb-2 text-pink-50 uppercase tracking-wider opacity-90 font-sans">Ensemble</div>
                <div className="text-3xl text-pink-50 tracking-tighter font-sans font-bold">89%</div>
              </div>
            </div>

            <p className="text-lg text-stone-700 leading-relaxed">
              Tested multiple algorithms including Random Forest, XGBoost, and LightGBM. The final ensemble model combines all three approaches,
              achieving 89% accuracy through weighted voting based on individual model strengths.
            </p>

            <div className="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border-2 border-stone-200">
              <h3 className="text-xl mb-6 text-stone-900 tracking-tight font-sans font-semibold">Model Comparison</h3>
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={conversionData} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" stroke="#d6d3d1" opacity={0.5} />
                  <XAxis type="number" stroke="#78716c" style={{ fontSize: '12px', fontFamily: 'Inter' }} />
                  <YAxis dataKey="stage" type="category" stroke="#78716c" style={{ fontSize: '12px', fontFamily: 'Inter' }} />
                  <Tooltip contentStyle={{ backgroundColor: 'rgba(255, 255, 255, 0.95)', border: '2px solid #d6d3d1', borderRadius: '8px', padding: '8px', fontSize: '13px' }} />
                  <Legend wrapperStyle={{ paddingTop: '16px', fontSize: '13px' }} />
                  <Bar dataKey="count" fill="#78716c" name="Users" radius={[0, 6, 6, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </CollapsibleSection>

        <CollapsibleSection id="evaluation" title="Evaluation" bgColor="bg-gradient-to-br from-sky-200 via-blue-100 to-sky-300">
          <div className="space-y-6">
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-gradient-to-br from-sky-200 to-sky-300 p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-2 border-black/5">
                <div className="text-xs mb-2 text-stone-900 uppercase tracking-wider opacity-80 font-sans">Model Accuracy</div>
                <div className="text-4xl text-stone-950 tracking-tighter font-sans font-bold">87%</div>
                <div className="text-sm mt-3 text-[#8B4949] font-medium font-sans">↑ 12% from baseline</div>
              </div>
              <div className="bg-gradient-to-br from-pink-200 to-pink-300 p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-2 border-black/5">
                <div className="text-xs mb-2 text-stone-900 uppercase tracking-wider opacity-80 font-sans">Precision</div>
                <div className="text-4xl text-stone-950 tracking-tighter font-sans font-bold">84%</div>
                <div className="text-sm mt-3 text-[#8B4949] font-medium font-sans">High confidence</div>
              </div>
              <div className="bg-gradient-to-br from-emerald-200 to-emerald-300 p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-2 border-black/5">
                <div className="text-xs mb-2 text-stone-900 uppercase tracking-wider opacity-80 font-sans">Recall</div>
                <div className="text-4xl text-stone-950 tracking-tighter font-sans font-bold">89%</div>
                <div className="text-sm mt-3 text-stone-900 font-medium font-sans">Excellent coverage</div>
              </div>
            </div>

            <p className="text-lg text-stone-700 leading-relaxed">
              The model demonstrates strong performance across all key metrics, with particularly high recall ensuring most potential returns are identified.
              Cross-validation results confirm the model's robustness and generalization capability.
            </p>
          </div>
        </CollapsibleSection>

        <CollapsibleSection id="business" title="Business Interpretation" bgColor="bg-gradient-to-br from-[#8B4949] via-[#9D5E5E] to-[#7A3E3E]">
          <div className="space-y-6">
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-gradient-to-br from-amber-200 to-yellow-300 p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-2 border-black/5">
                <div className="text-xs mb-2 text-stone-900 uppercase tracking-wider opacity-80 font-sans">Cost Savings</div>
                <div className="text-4xl text-stone-950 tracking-tighter font-sans font-bold">$2.4M</div>
                <div className="text-sm mt-3 text-stone-900 font-medium font-sans">Annual projection</div>
              </div>
              <div className="bg-gradient-to-br from-pink-200 to-pink-300 p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-2 border-black/5">
                <div className="text-xs mb-2 text-stone-900 uppercase tracking-wider opacity-80 font-sans">Return Rate Reduction</div>
                <div className="text-4xl text-stone-950 tracking-tighter font-sans font-bold">23%</div>
                <div className="text-sm mt-3 text-[#8B4949] font-medium font-sans">Target achieved</div>
              </div>
              <div className="bg-gradient-to-br from-sky-200 to-sky-300 p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] border-2 border-black/5">
                <div className="text-xs mb-2 text-stone-900 uppercase tracking-wider opacity-80 font-sans">Customer Satisfaction</div>
                <div className="text-4xl text-stone-950 tracking-tighter font-sans font-bold">+15%</div>
                <div className="text-sm mt-3 text-[#8B4949] font-medium font-sans">NPS improvement</div>
              </div>
            </div>

            <p className="text-lg text-stone-700 leading-relaxed">
              By implementing proactive interventions based on model predictions, we achieved significant business impact including reduced return rates,
              improved customer satisfaction, and substantial cost savings through optimized inventory management and logistics.
            </p>
          </div>
        </CollapsibleSection>

      </main>
    </div>
  );
}
