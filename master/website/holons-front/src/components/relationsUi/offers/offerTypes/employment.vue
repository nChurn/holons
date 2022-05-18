<template>
<div id="employmentModal" class="hm modal active">

      <div class="content big">
        <h2 class="title">offer boilerplate</h2>

        <div class="ui grid contract">


            <offer-templates v-if="!offer.preview" />


            <div class="ten wide column">

              <div id="combOffer">

                <input class="title"
                type="text" value="cotract name – edit me">

                <p>
                    <!-- juusst output sender handler first -->
                    @grintender or his representatives assign tasks within a scope discussed,
                    and <input class="hm legal" type="text" placeholder="Alex">
                    <!--<div class="ui inline multiple search selection dropdown">
                      <input type="hidden">
                      <div class="default text">select or add new</div>
                      <div class="menu">
                        <div class="item" data-value="elliot">
                          <img class="ui mini avatar image" src="https://semantic-ui.com/images/avatar/small/jenny.jpg">
                            Jenny Hess
                        </div>
                        <div class="item" data-value="elliot">
                          <img class="ui mini avatar image" src="https://semantic-ui.com/images/avatar/small/elliot.jpg">
                          Elliot Fu
                        </div>
                      </div>
                    </div>--> does the job as good as possible, tracking time at holons.me
                </p>


                <p>
                      That time is billed to <select class="hm legal" id="pet-select">
                      <option value="" selected>@grintender</option>
                      <option value="">@launcher</option>
                    </select>
                   at <input class="hm legal" type="number" value="250">
                    <select class="hm legal" id="pet-select">
                      <option value="" selected>RUB</option>
                      <option value="">USD</option>
                    </select>
                    <select class="hm legal" id="pet-select">
                      <option value="" selected>per hour</option>
                      <option value="">per item delivered</option>
                      <option value="">salary monthly</option>
                    </select>
                </p>


                <p>The commitment exists until canceled by either side.
                Invoicing is due every <input class="hm legal" type="number" value="4"> weeks
              </p>

                <!--<p>@user assummes NDA agreement</p>-->

                <div class="ui field">
                  <label for="">
                  <input
                    type="checkbox"
                    class="ui checkbox input"
                    v-model="offer.membershipSponsor"
                   />
                   I will pay for this user's account $14 monthly if he\she doesn't already have one.<br>
                   I understand that without paid account he\she won't be able to accept the offer. <br>
                 </label>
                </div>

                <div style="text-align:right;margin-bottom: 2rem">
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
  name: 'offerTypeEmployment',
  props: ['offer'],
  components: {
    disputeResolution,
    offerTemplates,
    // AddParagraph,
  },
}
</script>
