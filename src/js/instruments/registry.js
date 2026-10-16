/**
 * The Saac Financial Terminal - Universal Instrument Registry
 * Decoupled multi-asset schema: Gold, Nasdaq, S&P 500, Crypto, Forex, etc.
 * Allows adding any new tracker without modifying core charting or UI code.
 */

export class InstrumentRegistry {
  constructor() {
    this.instruments = new Map();
    this.activeInstrumentId = 'gold';
    this.listeners = [];
  }

  /**
   * Registers a new financial instrument configuration.
   * @param {object} instrumentConfig
   */
  register(instrumentConfig) {
    if (!instrumentConfig || !instrumentConfig.id) {
      throw new Error("Instrument config must have an 'id'");
    }
    this.instruments.set(instrumentConfig.id, instrumentConfig);
  }

  /**
   * Retrieves an instrument config by ID.
   * @param {string} id
   * @returns {object|null}
   */
  get(id) {
    return this.instruments.get(id) || null;
  }

  /**
   * Returns all registered instruments.
   * @returns {Array<object>}
   */
  getAll() {
    return Array.from(this.instruments.values());
  }

  /**
   * Returns the currently active instrument.
   * @returns {object}
   */
  getActive() {
    const inst = this.instruments.get(this.activeInstrumentId);
    if (!inst) {
      const first = this.instruments.values().next().value;
      return first || null;
    }
    return inst;
  }

  /**
   * Sets the active instrument by ID and notifies listeners.
   * @param {string} id
   */
  setActive(id) {
    if (!this.instruments.has(id)) {
      console.warn(`Instrument '${id}' not found in registry.`);
      return false;
    }
    this.activeInstrumentId = id;
    const inst = this.instruments.get(id);
    for (const listener of this.listeners) {
      try {
        listener(inst);
      } catch (e) {
        console.error("Error in instrument switch listener:", e);
      }
    }
    return true;
  }

  /**
   * Subscribes to instrument changes.
   * @param {Function} callback
   */
  subscribe(callback) {
    this.listeners.push(callback);
    return () => {
      this.listeners = this.listeners.filter(cb => cb !== callback);
    };
  }
}

export const registry = new InstrumentRegistry();

if (typeof window !== 'undefined') {
  window.InstrumentRegistry = InstrumentRegistry;
  window.instrumentRegistry = registry;
}
