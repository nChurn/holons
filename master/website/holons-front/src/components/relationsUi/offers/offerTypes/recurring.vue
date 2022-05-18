<template>
<div id="offerModal" class="hm modal active">

      <div class="content big">
        <h2 class="title">recurring offer boilerplate</h2>

        <div class="ui grid contract">

            <offer-templates v-if="!offer.preview" />

            <div class="ten wide column">

              <div id="combOffer">

                <input class="title"
                type="text" value="cotract name – edit me">

                <p>
                    <!-- juusst output sender handler first -->
                    @grintender enters in agreement with <input class="hm legal" type="text" placeholder="Alex">
                </p>

                <div style="text-align:right;margin-bottom: 2rem">
                  <a class="hm link">add paragraph describing the matter</a>
                </div>

                <p>
                  The payment due is <input class="hm legal" type="number" value="250">
                    <select class="hm legal" id="pet-select">
                      <option value="" selected>RUB</option>
                      <option value="">USD</option>
                    </select>
                </p>

                <div style="text-align:right;margin-bottom: 2rem">
                  <a class="hm link">add paragraph describing the payment terms</a>
                </div>

                <p>
                  The contract starts <select class="hm legal" id="pet-select">
                      <option value="" selected>immediately upon acceptance</option>
                      <option value="">immediatly upon first invoice paid</option>
                      <option value="">+ specify start date</option>
                    </select>

                  and is due in <input class="hm legal" type="number" value="30"> days.<br>
                  Soft deadline <input class="hm legal" type="number" value="25"> days.
                </p>

                <div style="text-align:right">
                  <a class="hm link">+ paragraph</a>
                </div>


              </div>

              <br><br>

              <a style="width:100%"
              class="ui basic button">preview</a>
                  <!--
                  <a class="hm link">save as template</a>
                  <a class="ui basic button">shadow sign</a>

                  <a class="ui basic button">ray to</a>
                -->

            </div>

            <dispute-resolution v-if="!offer.preview" />




        </div>

      </div>

    </div>
</template>


<script>
import offerTemplates from '../templates/offer-templates'
import disputeResolution from '../templates/dispute-resolution'
// import AddParagraph from '../AddParagraph'

export default {
  name: 'offerTypeRecurring',
  props: ['offer'],
  components: {
    disputeResolution,
    offerTemplates,
    // AddParagraph,
  },
}
</script>
