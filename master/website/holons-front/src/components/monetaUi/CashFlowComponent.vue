<template>
  <div style="margin:2rem">
    <h2>Cash Flow</h2>
    <table class="hm table">
      <thead>
        <tr>
          <th></th>
          <th v-for="month in months" :key="monthFormat(month.startDate)">{{ monthFormat(month.startDate) }}</th>
          <th>year total</th>
        </tr>
      </thead>

      <tbody>
        <tr>
          <td><strong>cash inflows</strong></td>
        </tr>

        <!-- sums of invoices paid $this month-->
        <tr v-for="inflow in inflows" :key="inflow.name">
          <td>{{ inflow.name }}</td>
          <td v-for="value in inflow.values" :key="value">${{ value || 0 }}</td>
          <td> {{ inflow.values.length ? '$' + inflow.values.reduce((a, v) => a + v) : '' }} </td>
        </tr>

        <tr>
          <td><strong>cash outflows</strong></td>
        </tr>
        <tr v-for="outflow in outflows" :key="outflow.name">
          <td>{{ outflow.name }}</td>
          <td v-for="value in outflow.values" :key="value">${{ value || 0 }}</td>
          <td> {{ outflow.values.length  ? '$' + outflow.values.reduce((a, v) => a + v) : '' }} </td>
        </tr>
        <tr>
        <tr>
          <!-- inflow minus outflow -->
          <td><strong>subtotal:</strong></td>
          <td v-for="month in months" :key="monthFormat(month.startDate)">${{ monthSubtotal(month) }}</td>
          <td>${{ months.map(m => monthSubtotal(m)).reduce((a, v) => a + v) }}</td>
        </tr>

        <tr>
          <td><h3 style="color:red">profit margin</h3> </td>
        </tr>

        <tr>
          <td>dividends on #equity paid</td>
          <!-- sums of invoices paid $this month-->
          <td>0</td>
          <td>0</td>
          <td>$50</td>
          <td>0</td>
          <td>0</td>
          <td>$50</td>
          <td>0</td>
          <td>0</td>
          <td>$50</td>
          <td>0</td>
          <td>0</td>
          <td>$50</td>
        </tr>

        <tr>
          <!-- inflow minus outflow -->
          <td><strong>net inflow:</strong></td>
          <td>X</td>
          <td>XX</td>
          <td>XXX</td>
          <td>X</td>
          <td>XX</td>
          <td>XXX</td>
          <td>X</td>
          <td>XX</td>
          <td>XXX</td>
          <td>X</td>
          <td>XX</td>
          <td>XXX</td>
        </tr>

        <tr>
          <!-- inflow minus outflow -->
          <td><strong>opening balance:</strong></td>
          <td>X</td>
          <td>XX</td>
          <td>XXX</td>
          <td>X</td>
          <td>XX</td>
          <td>XXX</td>
          <td>X</td>
          <td>XX</td>
          <td>XXX</td>
          <td>X</td>
          <td>XX</td>
          <td>XXX</td>
        </tr>

        <tr>
          <!-- inflow minus outflow -->
          <td><strong>gross closing balance:</strong></td>
          <td>X</td>
          <td>XX</td>
          <td>XXX</td>
          <td>X</td>
          <td>XX</td>
          <td>XXX</td>
          <td>X</td>
          <td>XX</td>
          <td>XXX</td>
          <td>X</td>
          <td>XX</td>
          <td>XXX</td>
        </tr>
      </tbody>
    </table>

    <img src="https://sun9-33.userapi.com/impg/CGsguoyxXqcNNtkpBQmmXrDSBNEYXK21f_tLIQ/xALOmHQrFPM.jpg?size=1576x784&quality=96&sign=54784cfac653b6a77a41e0d4235e9d52&type=album"
    width="auto" height="250px">

  <!--
    cash inflow

      sales i.e. invoices, right?

    cash outflow

      variable costs
        and one-off expenses
        payroll

      fixed costs


    subtotal x [ 12 month by default, seasons, custom ]

    total x [ 12 month by default, seasons, custom ]
  -->


  </div>

</template>

<script>
export default {
    name: "CashFlowComponent",

    components: {},

    props: {},

    data() {
        return {
            months: [
                {
                    startDate: new Date(new Date().getFullYear(), 0, 1),
                },
                {
                    startDate: new Date(new Date().getFullYear(), 1, 1),
                },
                {
                    startDate: new Date(new Date().getFullYear(), 2, 1),
                },
                {
                    startDate: new Date(new Date().getFullYear(), 3, 1),
                },
                {
                    startDate: new Date(new Date().getFullYear(), 4, 1),
                },
                {
                    startDate: new Date(new Date().getFullYear(), 5, 1),
                },
                {
                    startDate: new Date(new Date().getFullYear(), 6, 1),
                },
                {
                    startDate: new Date(new Date().getFullYear(), 7, 1),
                },
                {
                    startDate: new Date(new Date().getFullYear(), 8, 1),
                },
                {
                    startDate: new Date(new Date().getFullYear(), 9, 1),
                },
                {
                    startDate: new Date(new Date().getFullYear(), 10, 1),
                },
                {
                    startDate: new Date(new Date().getFullYear(), 11, 1),
                },
            ],
            inflows: [
                {
                    name: "sales",
                    values: [
                        100, 500, 1000, 100, 500, 1000, 100, 500, 1000, 100, 500, 1000,
                    ],
                },
            ],
            outflows: [
                {
                    name: "fixed costs",
                    values: [],
                },
                {
                    name: "variable costs",
                    values: [],
                },
                {
                    name: "payroll",
                    values: [10, 50, 100, 10, 50, 100, 10, 50, 100, 10, 50, 100 ],
                },
                {
                    name: "one-off expenses",
                    values: [0, 0, 50, 0, 0, 50, 0, 0, 50, 0, 0, 50],
                },
            ],

            fixedCosts: [],
            variableCosts: []
        };
    },
    computed: {
        apiUrl() {
            return window.location.origin + "/api/moneta";
        },
        activeContext() {
            return this.$parent.activeContext;
        },
        costsComponent(){
            return this.$parent.$children.find(c => c.$options.name == 'LoansDepositsComponent')
        },
        now(){
            return (new Date())
        }        
    },
    watch: {
        activeContext: {
            handler(){
                this.updateCosts()
            },
            immediate: true,
        },
        fixedCosts: {
            handler(){
                this.updateCosts()
            },
            immediate: true,
        },
        variableCosts: {
            handler(){
                this.updateCosts()
            },
            immediate: true,
        },
    },
    methods: {
        monthFormat(date) {
            return Intl.DateTimeFormat("en", {
                month: "short",
                year: "numeric",
            }).format(date);
        },
        monthSubtotal(month) {
            return (
                this.inflows
                    .map((inflow) =>
                        inflow.values[month.startDate.getMonth()]
                            ? inflow.values[month.startDate.getMonth()]
                            : 0
                    )
                    .reduce((a, v) => a + v) -
                this.outflows
                    .map((outflow) =>
                        outflow.values[month.startDate.getMonth()]
                            ? outflow.values[month.startDate.getMonth()]
                            : 0
                    )
                    .reduce((a, v) => a + v)
            );
        },
        updateCosts(){
            const fixedCostsValues = (new Array(12)).fill(0)
            const variableCostsValues = (new Array(12)).fill(0)

            for(let fixedCost of this.fixedCosts.filter(c => c.context_id == this.activeContext.id)){
                if((new Date(fixedCost.started_at)).getFullYear() < this.now.getFullYear()) continue
                for(let i = (new Date(fixedCost.started_at)).getMonth(); i <= (fixedCost.finished_at ? (new Date(fixedCost.finished_at)).getMonth() : this.months.length - 1); i++){
                    if(typeof(fixedCostsValues[i]) == 'undefined') fixedCostsValues[i] = 0

                    fixedCostsValues[i] += fixedCost.amount
                }
            }

            for(let variableCost of this.variableCosts.filter(c => c.context_id == this.activeContext.id)){
                let date = new Date(variableCost.date)

                if(date.getFullYear() < this.now.getFullYear()) continue;

                if(typeof(variableCostsValues[date.getMonth()]) == 'undefined') variableCostsValues[date.getMonth()] = 0
                
                variableCostsValues[date.getMonth()] += variableCost.amount
            }

            this.outflows.find(o => o.name == 'fixed costs').values = fixedCostsValues
            this.outflows.find(o => o.name == 'variable costs').values = variableCostsValues
            this.$forceUpdate()
        }
    },
    mounted(){
        for(let costsType of ['variable', 'fixed']){
            fetch(this.apiUrl + `/${costsType}-costs`)
            .then(res => res.ok && res.json())
            .then(res => {
                if(!res) return

                this[`${costsType}Costs`] = res
                // this.updateCosts()      
            })

        }
    }   
};
</script>

<style scoped>
</style>

