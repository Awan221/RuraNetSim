<template>
  <div class="network-type-selector">
    <div class="form-group">
      <label for="networkType">Type de réseau</label>
      <select 
        id="networkType" 
        v-model="networkType" 
        class="form-control"
        @change="onNetworkTypeChange"
      >
        <option value="4g">4G/LTE</option>
        <option value="5g">5G</option>
      </select>
    </div>

    <!-- Paramètres spécifiques à la 5G -->
    <div v-if="networkType === '5g'" class="5g-params">
      <div class="form-group">
        <label for="scenario">Scénario de déploiement</label>
        <select 
          id="scenario" 
          v-model="scenario" 
          class="form-control"
          @change="onScenarioChange"
        >
          <option 
            v-for="option in scenarioOptions" 
            :key="option.value" 
            :value="option.value"
          >
            {{ option.label }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="losCondition">Condition de visibilité</label>
        <select 
          id="losCondition" 
          v-model="los_condition" 
          class="form-control"
          @change="onParamChange"
        >
          <option value="LOS">Ligne de vue (LOS)</option>
          <option value="NLOS">Sans ligne de vue (NLOS)</option>
        </select>
      </div>

      <div v-if="showAdvancedParams" class="advanced-params">
        <div class="form-group">
          <label :for="'h_bs' + _uid">Hauteur de la station de base (m)</label>
          <input 
            :id="'h_bs' + _uid"
            v-model.number="h_bs" 
            type="number" 
            min="1" 
            step="0.1" 
            class="form-control"
            @change="onParamChange"
          >
        </div>

        <div class="form-group">
          <label :for="'h_ut' + _uid">Hauteur de l'utilisateur (m)</label>
          <input 
            :id="'h_ut' + _uid"
            v-model.number="h_ut" 
            type="number" 
            min="0.5" 
            step="0.1" 
            class="form-control"
            @change="onParamChange"
          >
        </div>

        <div v-if="['RMa', 'UMa'].includes(scenario)" class="form-group">
          <label :for="'h' + _uid">Hauteur moyenne des bâtiments (m)</label>
          <input 
            :id="'h' + _uid"
            v-model.number="h" 
            type="number" 
            min="1" 
            step="0.1" 
            class="form-control"
            @change="onParamChange"
          >
        </div>

        <div v-if="['RMa', 'UMa'].includes(scenario)" class="form-group">
          <label :for="'w' + _uid">Largeur moyenne des routes (m)</label>
          <input 
            :id="'w' + _uid"
            v-model.number="w" 
            type="number" 
            min="1" 
            step="0.1" 
            class="form-control"
            @change="onParamChange"
          >
        </div>
      </div>

      <button 
        class="btn btn-link btn-sm p-0 mb-3" 
        @click="toggleAdvancedParams"
      >
        {{ showAdvancedParams ? 'Masquer les paramètres avancés' : 'Afficher les paramètres avancés' }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NetworkTypeSelector',
  
  props: {
    modelValue: {
      type: Object,
      required: true
    }
  },
  
  emits: ['update:modelValue', 'network-type-change', 'scenario-change'],
  
  data() {
    // Initialiser avec les valeurs du modèle ou des valeurs par défaut
    const initialValues = {
      networkType: '5g',
      scenario: 'UMa',
      los_condition: 'LOS',
      h_bs: 10.0,
      h_ut: 1.5,
      h: 20.0,
      w: 20.0
    };
    
    // Fusionner avec les valeurs fournies par le parent
    const mergedValues = { ...initialValues, ...this.modelValue };
    
    return {
      ...mergedValues,
      showAdvancedParams: false,
      scenarioOptions: [
        { value: 'UMa', label: 'Urbain Macro (UMa)' },
        { value: 'UMi', label: 'Urbain Micro (UMi)' },
        { value: 'RMa', label: 'Rural Macro (RMa)' },
        { value: 'InH-Office', label: 'Intérieur - Bureau' },
        { value: 'InH-ShoppingMall', label: 'Intérieur - Centre commercial' }
      ]
    };
  },
  
  created() {
    // Initialiser avec les valeurs par défaut
    this.emitUpdate();
  },
  
  methods: {
    toggleAdvancedParams() {
      this.showAdvancedParams = !this.showAdvancedParams;
    },
    
    onNetworkTypeChange() {
      this.emitUpdate();
      this.$emit('network-type-change', this.networkType);
    },
    
    onScenarioChange() {
      this.emitUpdate();
      this.$emit('scenario-change', this.scenario);
    },
    
    onParamChange() {
      this.emitUpdate();
    },
    
    emitUpdate() {
      const updatedData = {
        networkType: this.networkType,
        scenario: this.scenario,
        los_condition: this.los_condition,
        h_bs: parseFloat(this.h_bs),
        h_ut: parseFloat(this.h_ut),
        h: parseFloat(this.h),
        w: parseFloat(this.w)
      };
      
      // Émettre l'événement de mise à jour
      this.$emit('update:modelValue', updatedData);
    }
  }
};
</script>

<style scoped>
.network-type-selector {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.advanced-params {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 0.25rem;
  border: 1px solid #dee2e6;
}

.btn-link {
  color: #0d6efd;
  text-decoration: none;
}

.btn-link:hover {
  text-decoration: underline;
}
</style>
