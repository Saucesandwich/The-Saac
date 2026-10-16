/**
 * The Saac Financial Terminal - Universal Instrument Registry
 * Decoupled multi-asset schema: Gold, Major Indices, ETFs, Commodities, Sovereign Country Bonds, and Forex.
 * Allows adding any new tracker without modifying core charting or UI code.
 */

import { MACRO_CATALOG } from './catalog.js';

export class InstrumentRegistry {
  constructor() {
    this.instruments = new Map();
    this.activeInstrumentId = 'gold';
    this.listeners = [];

    // Register all catalog instruments automatically
    if (Array.isArray(MACRO_CATALOG)) {
      for (const inst of MACRO_CATALOG) {
        this.register(inst);
      }
    }
  }

  /**
   * Registers a new financial instrument configuration.
   * @param {object} instrumentConfig
   */
  register(instrumentConfig) {
    if (!instrumentConfig || !instrumentConfig.id) {
      throw new Error("Instrument config must have an 'id'");
    }
    this.instruments.set(instrumentConfig.id.toLowerCase(), instrumentConfig);
    if (instrumentConfig.symbol) {
      this.instruments.set(instrumentConfig.symbol.toLowerCase(), instrumentConfig);
    }
    if (instrumentConfig.ticker) {
      this.instruments.set(instrumentConfig.ticker.toLowerCase(), instrumentConfig);
    }
  }

  /**
   * Retrieves an instrument config by ID, symbol, or ticker.
   * @param {string} id
   * @returns {object|null}
   */
  get(id) {
    if (!id) return null;
    return this.instruments.get(String(id).toLowerCase()) || null;
  }

  /**
   * Returns all unique registered instruments.
   * @returns {Array<object>}
   */
  getAll() {
    const seen = new Set();
    const unique = [];
    for (const inst of this.instruments.values()) {
      if (!seen.has(inst.id)) {
        seen.add(inst.id);
        unique.append ? unique.append(inst) : unique.push(inst);
      }
    }
    return unique;
  }

  /**
   * Returns all instruments within a specific category.
   * @param {string} category - 'commodities', 'indices', 'etfs', 'bonds', 'forex'
   * @returns {Array<object>}
   */
  getByCategory(category) {
    if (!category || category === 'all') return this.getAll();
    return this.getAll().filter(i => i.category === category);
  }

  /**
   * Returns the currently active instrument.
   * @returns {object}
   */
  getActive() {
    const inst = this.instruments.get(this.activeInstrumentId.toLowerCase());
    if (!inst) {
      const first = this.getAll()[0];
      return first || null;
    }
    return inst;
  }

  /**
   * Sets the active instrument by ID and notifies listeners.
   * @param {string} id
   */
  setActive(id) {
    const inst = this.get(id);
    if (!inst) {
      console.warn(`Instrument '${id}' not found in registry.`);
      return false;
    }
    this.activeInstrumentId = inst.id;
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
