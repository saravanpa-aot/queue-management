<template>
  <b-modal
    v-model="modal"
    hide-header
    size="md"
    modal-class="q-modal"
    body-class="q-modal"
    no-close-on-backdrop
    no-close-on-esc
    @shown="show"
  >
    <template slot="modal-footer">
      <div class="d-flex flex-row-reverse">
        <b-button
          v-if="
            this.recurring_input_state === 'notes' ||
            this.single_input_state === 'notes'
          "
          variant="primary"
          class="ml-2"
          size="md"
          @click="deleteApptWarning"
        >
          Submit</b-button
        >
        <b-button v-else class="ml-2" size="md" disabled> Submit </b-button>
        <b-button
          v-if="this.recurring_input_state === 'event_information'"
          variant="primary"
          class="w-100 ml-2"
          size="md"
          v-b-toggle.recurring-dates-collapse
          @click="generateRule"
        >
          Next
        </b-button>
        <b-button
          v-else-if="this.single_input_state === 'event_information'"
          variant="primary"
          class="w-100 ml-2"
          size="md"
          @click="nextSingleNotes"
        >
          Next
        </b-button>
        <b-button
          v-else-if="this.recurring_input_state === 'audit_information'"
          variant="primary"
          class="w-100 ml-2"
          size="md"
          @click="nextRecurringNotes"
        >
          Next
        </b-button>
        <b-button
          v-else-if="
            this.single_input_state === 'notes' ||
            this.recurring_input_state === 'notes'
          "
          disabled
          class="w-100 ml-2"
          size="md"
        >
          Next
        </b-button>
        <b-button @click="cancel" size="md"> Cancel </b-button>
      </div>
    </template>
    <span style="font-size: 1.75rem">Schedule Appointment Blackout</span><br />
    <b-form>
      <b-collapse id="collapse-event-selection">
        <b-card>
          <b-form-row class="mb-2">
            <label>Step 1: Select Event Type</label>
          </b-form-row>
          <b-form-row>
            <b-col class="w-50 mb-1">
              <b-button
                variant="primary"
                class="w-100 mb-1"
                v-b-toggle.collapse-single-event
                @click="setRecurring"
              >
                Create Single Blackout
              </b-button>
            </b-col>
            <b-col v-if="is_recurring_enabled" class="w-50">
              <b-button
                variant="primary"
                class="w-100 mb-1"
                v-b-toggle.collapse-recurring-events
                @click="setSingle"
              >
                Create Recurring Blackout
              </b-button>
            </b-col>
          </b-form-row>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-single-event">
        <b-card class="mt-2 mb-2">
          <b-form-row style="justify-content: center">
            <h4>Single Event</h4>
          </b-form-row>
          <b-form-row class="mb-2">
            <label stlye="font-weight: bold;">Step 2: Event Information</label>
          </b-form-row>
          <b-form-row class="mb-2">
            <b-col cols="6">
              <label>User Name</label><br />
              <b-form-input v-model="this.user_name" disabled />
            </b-col>
            <b-col cols="6">
              <label>Contact Information (optional)</label>
              <b-form-input v-model="this.user_contact_info" />
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout Date:</label>
                <font-awesome-icon
                  v-if="this.blackout_date !== null"
                  icon="check"
                  style="fontsize: 1rem; color: green"
                />
                <DatePicker
                  v-model="blackout_date"
                  id="appointment_blackout_date"
                  type="date"
                  lang="en"
                  class="w-100"
                  @change="checkSingleInput"
                  @input="checkSingleInput"
                  @clear="checkSingleInput"
                >
                </DatePicker>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout Start Time:</label>
                <font-awesome-icon
                  v-if="this.start_time !== null"
                  icon="check"
                  style="fontsize: 1rem; color: green"
                />
                <DatePicker
                  v-model="start_time"
                  id="appointment_blackout_start_time"
                  :time-picker-options="{
                    start: '8:00',
                    step: '00:30',
                    end: '16:30',
                  }"
                  lang="en"
                  format="h:mm a"
                  autocomplete="off"
                  :editable="false"
                  placeholder="Select Start Time"
                  class="w-100"
                  type="time"
                  @change="checkSingleInput"
                  @input="checkSingleInput"
                  @clear="checkSingleInput"
                >
                </DatePicker>
              </b-form-group>
            </b-col>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout End Time:</label>
                <font-awesome-icon
                  v-if="this.end_time !== null"
                  icon="check"
                  style="fontsize: 1rem; color: green"
                />
                <DatePicker
                  v-model="end_time"
                  id="appointment_blackout_end_time"
                  :time-picker-options="{
                    start: '8:30',
                    step: '00:30',
                    end: '17:00',
                  }"
                  lang="en"
                  format="h:mm a"
                  autocomplete="off"
                  :editable="false"
                  placeholder="Select End Time"
                  class="w-100"
                  type="time"
                  @change="checkSingleInput"
                  @input="checkSingleInput"
                  @clear="checkSingleInput"
                >
                </DatePicker>
              </b-form-group>
            </b-col>
          </b-form-row>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-recurring-events">
        <b-card class="mt-2">
          <b-form-row style="justify-content: center">
            <h4>Recurring Event</h4>
          </b-form-row>
          <b-form-row class="mb-2">
            <label style="font-weight: bold">Step 2: Event Information</label>
          </b-form-row>
          <b-form-row class="mb-2">
            <b-col cols="6">
              <label>User Name:</label><br />
              <b-form-input v-model="this.user_name" disabled />
            </b-col>
            <b-col cols="6">
              <label>Contact Information (optional):</label>
              <b-form-input v-model="this.user_contact_info" />
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout Start Time:</label>
                <font-awesome-icon
                  v-if="this.recurring_start_time !== null"
                  icon="check"
                  style="fontsize: 1rem; color: green"
                />
                <DatePicker
                  v-model="recurring_start_time"
                  id="recurring_blackout_start_time"
                  :time-picker-options="{
                    start: '8:00',
                    step: '00:30',
                    end: '16:30',
                  }"
                  lang="en"
                  format="h:mm a"
                  autocomplete="off"
                  :editable="false"
                  placeholder="Select Start Time"
                  class="w-100"
                  type="time"
                  @change="checkRecurringInput"
                  @input="checkRecurringInput"
                  @clear="checkRecurringInput"
                >
                </DatePicker>
              </b-form-group>
            </b-col>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout End Time:</label>
                <font-awesome-icon
                  v-if="this.recurring_end_time !== null"
                  icon="check"
                  style="fontsize: 1rem; color: green"
                />
                <DatePicker
                  v-model="recurring_end_time"
                  id="recurring_blackout_end_time"
                  :time-picker-options="{
                    start: '8:30',
                    step: '00:30',
                    end: '17:00',
                  }"
                  lang="en"
                  format="h:mm a"
                  autocomplete="off"
                  :editable="false"
                  placeholder="Select End Time"
                  class="w-100"
                  type="time"
                  @change="checkRecurringInput"
                  @input="checkRecurringInput"
                  @clear="checkRecurringInput"
                >
                </DatePicker>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout Start Date:</label>
                <font-awesome-icon
                  v-if="this.recurring_start_date !== null"
                  icon="check"
                  style="fontsize: 1rem; color: green"
                />
                <DatePicker
                  id="recurring_start_date"
                  class="w-100"
                  lang="en"
                  v-model="recurring_start_date"
                  placeholder="Select Start Date"
                  @change="checkRecurringInput"
                  @input="checkRecurringInput"
                  @clear="checkRecurringInput"
                >
                </DatePicker>
              </b-form-group>
            </b-col>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout End Date:</label>
                <font-awesome-icon
                  v-if="this.recurring_end_date !== null"
                  icon="check"
                  style="fontsize: 1rem; color: green"
                />
                <DatePicker
                  id="recurring_end_date"
                  class="w-100"
                  lang="en"
                  v-model="recurring_end_date"
                  placeholder="Select End Date"
                  @change="checkRecurringInput"
                  @input="checkRecurringInput"
                  @clear="checkRecurringInput"
                >
                </DatePicker>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-form-group class="mt-0 ml-1">
              <label>Frequency:</label>
              <font-awesome-icon
                v-if="this.selected_frequency.length === 1"
                icon="check"
                style="fontsize: 1rem; color: green"
              />
              <font-awesome-icon
                v-if="this.selected_frequency.length > 1"
                icon="exclamation-triangle"
                style="fontsize: 1rem; color: #ffc32b"
              />
              <b-form-checkbox-group
                id="frequency-checkboxes"
                v-model="selected_frequency"
                @input="checkRecurringInput"
              >
                <!--                <b-form-checkbox :value="yearly">Yearly</b-form-checkbox>-->
                <!--                <b-form-checkbox :value="monthly">Monthly</b-form-checkbox>-->
                <b-form-checkbox :value="weekly">Weekly</b-form-checkbox>
                <b-form-checkbox :value="daily">Daily</b-form-checkbox>
              </b-form-checkbox-group>
            </b-form-group>
          </b-form-row>
          <b-form-group>
            <label>Select Weekdays:</label>
            <font-awesome-icon
              v-if="this.selected_weekdays.length >= 1"
              icon="check"
              style="fontsize: 1rem; color: green"
            />
            <b-form-checkbox-group
              id="weekday-checkboxes"
              v-model="selected_weekdays"
              @input="checkRecurringInput"
            >
              <b-form-checkbox :value="monday">Mon.</b-form-checkbox>
              <b-form-checkbox :value="tuesday">Tues.</b-form-checkbox>
              <b-form-checkbox :value="wednesday">Wed.</b-form-checkbox>
              <b-form-checkbox :value="thursday">Thurs.</b-form-checkbox>
              <b-form-checkbox :value="friday">Fri.</b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>
          <b-form-group>
            <b-form-row>
              <label style="font-weight: bold" class="mt-0"
                >Number of Occurences(optional):
              </label>
              <span v-if="this.selected_count !== ''"
                >&nbsp; Limited to {{ this.selected_count }} occurences.</span
              >
              <font-awesome-icon
                v-if="this.selected_count !== ''"
                icon="check"
                style="fontsize: 1rem; color: green"
                class="ml-1"
              />
            </b-form-row>
            <b-form-row>
              <b-col cols="6">
                <b-form-input
                  type="number"
                  class="mb-1 w-100"
                  v-model="selected_count"
                />
              </b-col>
            </b-form-row>
          </b-form-group>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-information-audit">
        <b-card class="mb-2">
          <b-form-group>
            <b-form-row style="justify-content: center">
              <h4>Recurring Event</h4>
            </b-form-row>
            <b-form-row class="mb-2">
              <label stlye="font-weight: bold;"
                >Step 2 (continued): Confirm Recurring Event Dates</label
              >
            </b-form-row>
            <b-form-row>
              <b-col cols="12">
                <b-button
                  variant="primary"
                  class="w-100 mb-2"
                  v-b-toggle.recurring-rule-collapse
                >
                  View Recurring Event Info
                </b-button>
              </b-col>
            </b-form-row>
            <b-form-row class="mb-0">
              <b-collapse
                id="recurring-rule-collapse"
                class="mb-2 ml-2"
                visible
              >
                {{ this.rrule_text }}
              </b-collapse>
            </b-form-row>
            <b-form-row>
              <b-col cols="12">
                <b-button
                  variant="primary"
                  class="w-100 mb-2"
                  v-b-toggle.recurring-dates-collapse
                >
                  View Recurring Dates ({{ this.rrule_array.length }})
                </b-button>
              </b-col>
            </b-form-row>
            <b-form-row>
              <b-collapse id="recurring-dates-collapse" class="mb-2">
                <div style="height: 75px; overflow-y: scroll; margin: 0px">
                  <ul
                    class="list-group"
                    v-for="date in this.rrule_array"
                    style="justify-content: center"
                    :key="date.start"
                  >
                    <li class="list-group-item">
                      <b>Event:</b> {{ formatStartDate(date.start) }} until
                      {{ formatEndDate(date.end) }}
                    </li>
                  </ul>
                </div>
              </b-collapse>
            </b-form-row>
          </b-form-group>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-blackout-notes">
        <b-card class="mt=2">
          <b-form-row style="justify-content: center">
            <h4 v-if="this.single_input_boolean">Single Event</h4>
            <h4 v-if="this.recurring_input_boolean">Recurring Event</h4>
          </b-form-row>
          <b-form-row>
            <label
              v-if="this.recurring_input_boolean"
              stlye="font-weight: bold;"
            >
              Step 3 (optional): Event Notes. <br /><em
                >This will be included in cancellation email.</em
              >
            </label>
            <label v-if="this.single_input_boolean" stlye="font-weight: bold;">
              Step 2 (optional): Event Notes. <br /><em
                >This will be included in cancellation email.</em
              >
            </label>
            <font-awesome-icon
              v-if="this.notes !== ''"
              icon="check"
              style="fontsize: 1rem; color: green"
            />
          </b-form-row>
          <b-form-row>
            <b-textarea
              v-model="notes"
              id="single_appointment_blackout_notes"
              placeholder="Enter notes about blackout period"
              rows="3"
              maxlength="255"
              max-rows="6"
              size="md"
            >
            </b-textarea>
          </b-form-row>
        </b-card>
      </b-collapse>
    </b-form>
    <v-dialog
      v-model="confirmDialog"
      max-width="400"
    >
      <v-card>
        <v-card-title class="headline">
         Warning
        </v-card-title>
        <v-card-text>
          {{ this.warning_text }}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="red darken-1"
            text
            @click="confirmBlackout(false)"
          >
            No
          </v-btn>
          <v-btn
            color="red darken-1"
            text
            @click="confirmBlackout(true)"
          >
            Yes
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </b-modal>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import DatePicker from 'vue2-datepicker'

import { RRule } from 'rrule'
import moment from 'moment'

import { namespace } from 'vuex-class'
const appointmentsModule = namespace('appointmentsModule')

@Component({
  components: {
    DatePicker
  }
})
export default class AppointmentBlackoutModal extends Vue {
  @appointmentsModule.State('showAppointmentBlackoutModal') private showAppointmentBlackoutModal!: any
  @appointmentsModule.State('appointments') private myappointments!: any

  @appointmentsModule.Getter('is_recurring_enabled') private is_recurring_enabled!: any;

  @appointmentsModule.Action('getAppointments') public getAppointments: any
  @appointmentsModule.Action('postAppointment') public postAppointment: any

  @appointmentsModule.Mutation('toggleAppointmentBlackoutModal') public toggleAppointmentBlackoutModal: any

  public blackout_date: any = null
  public start_time: any = null
  public end_time: any = null
  public notes: any = ''
  public user_name: any = ''
  public user_contact_info: any = ''
  public selected_frequency: any = []
  public selected_weekdays: any = []
  public selected_count: any = ''
  public recurring_start_time: any = null
  public recurring_end_time: any = null
  public recurring_start_date: any = null
  public recurring_end_date: any = null
  public recurring_array: any = ''
  public yearly: any = RRule.YEARLY
  public monthly: any = RRule.MONTHLY
  public weekly: any = RRule.WEEKLY
  public daily: any = RRule.DAILY
  public monday: any = RRule.MO
  public tuesday: any = RRule.TU
  public wednesday: any = RRule.WE
  public thursday: any = RRule.TH
  public friday: any = RRule.FR
  public single_blackout_boolean: any = true
  public recurring_blackout_boolean: any = true
  public rrule_array: any = []
  public filtered_appt: any = []
  public filtered_appt_start: any = []
  public filtered_appt_end: any = []
  public rrule_text: any = ''
  public recurring_input_boolean: any = false
  public single_input_boolean: any = false
  public next_boolean: any = false
  public single_input_state: any = ''
  public recurring_input_state: any = ''
  public warning_text: any = ''
  private confirmDialog: boolean = false
  public appt_overlap: any = 0

  get modal () {
    return this.showAppointmentBlackoutModal
  }

  set modal (e) {
    this.toggleAppointmentBlackoutModal(e)
  }

  hideCollapse (div_id) {
    const elementDivId = document.getElementById(div_id)
    if (elementDivId) {
      if (elementDivId.classList.contains('show')) {
        this.$root.$emit('bv::toggle::collapse', div_id)
      }
    }
  }

  showCollapse (div_id) {
    const elementDivId = document.getElementById(div_id)
    if (elementDivId) {
      if (elementDivId.style.display === 'none') {
        this.$root.$emit('bv::toggle::collapse',
          div_id)
      }
    }
  }

  show () {
    this.showCollapse('collapse-event-selection')
    this.hideCollapse('collapse-single-event')
    this.hideCollapse('collapse-information-audit')
    this.hideCollapse('collapse-blackout-notes')
    // clear single event information
    this.start_time = null
    this.end_time = null
    this.blackout_date = null

    // clear recurring event information
    this.recurring_start_date = null
    this.recurring_end_date = null
    this.recurring_start_time = null
    this.recurring_end_time = null
    this.selected_frequency = []
    this.selected_weekdays = []
    this.selected_count = ''
    this.notes = ''
  }

  cancel () {
    this.recurring_blackout_boolean = true
    this.single_blackout_boolean = true
    this.single_input_boolean = false
    this.recurring_input_boolean = false
    this.rrule_text = ''
    this.rrule_array = []
    this.toggleAppointmentBlackoutModal(false)
  }

  private async confirmBlackout (isAgree: boolean) {
    if (isAgree) {
      this.submit()
      this.confirmDialog = false
    } else {
      this.confirmDialog = false
      this.rrule_text = ''
      this.rrule_array = []
      this.recurring_input_state = ''
      this.single_input_boolean = ''
    }
  }

  private async countApptWarning (e) {
    this.filtered_appt = this.myappointments.filter(appt => appt.blackout_flag === 'N' && 
                                                    moment(appt.start_time).format('YYYY-MM-DD HH:mm:ssZ') >= e.start_time &&
                                                    moment(appt.end_time).format('YYYY-MM-DD HH:mm:ssZ') <= e.end_time)
    
    this.filtered_appt_start = this.myappointments.filter(appt => appt.blackout_flag === 'N' && 
                                                          moment(appt.start_time).format('YYYY-MM-DD HH:mm:ssZ') < e.start_time &&
                                                          moment(appt.end_time).format('YYYY-MM-DD HH:mm:ssZ') > e.start_time)
    
    this.filtered_appt_end = this.myappointments.filter(appt => appt.blackout_flag === 'N' && 
                                                        moment(appt.start_time).format('YYYY-MM-DD HH:mm:ssZ') < e.end_time &&
                                                        moment(appt.end_time).format('YYYY-MM-DD HH:mm:ssZ') > e.end_time)
    
    this.appt_overlap = this.appt_overlap + this.filtered_appt.length + this.filtered_appt_start.length + this.filtered_appt_end.length
  }

  deleteApptWarning () {
    // INC0056259 - Popup Warning message before committing Blackouts
    this.appt_overlap = 0
    const date = moment(this.blackout_date).clone().format('YYYY-MM-DD')
    const start = moment(this.start_time).clone().format('HH:mm:ss')
    const start_date = moment(date + ' ' + start).format('YYYY-MM-DD HH:mm:ssZ')
    const end = moment(this.end_time).clone().format('HH:mm:ss')
    const end_date = moment(date + ' ' + end).format('YYYY-MM-DD HH:mm:ssZ')
    const uuidv4 = require('uuid/v4')
    const recurring_uuid = uuidv4()
    if (this.rrule_array.length > 0) {
      this.rrule_array.forEach(item => {
        const e: any = {
          start_time: item.start,
          end_time: item.end,
          citizen_name: this.user_name,
          contact_information: this.user_contact_info,
          blackout_flag: 'Y',
          recurring_uuid: recurring_uuid
        }
        if (this.notes) {
          e.comments = this.notes
        }
        this.countApptWarning(e)
      })
    } else if (this.rrule_array.length === 0) {
      const e: any = {
        start_time: start_date,
        end_time: end_date,
        citizen_name: this.user_name,
        contact_information: this.user_contact_info,
        blackout_flag: 'Y'
      }
      if (this.notes) {
        e.comments = this.notes
      }
      this.countApptWarning(e)
    }
    if (this.appt_overlap > 0) {
      this.warning_text = "There is " + this.appt_overlap + " appointment(s) that will be cancelled due to Blackout. Are you sure you want to create the Blackout?"
      this.confirmDialog=true;
      this.toggleAppointmentBlackoutModal(false);
    } else {
      this.submit()
    }
  }

  submit () {
    const date = moment(this.blackout_date).clone().format('YYYY-MM-DD')
    const start = moment(this.start_time).clone().format('HH:mm:ss')
    const start_date = moment(date + ' ' + start).format('YYYY-MM-DD HH:mm:ssZ')
    const end = moment(this.end_time).clone().format('HH:mm:ss')
    const end_date = moment(date + ' ' + end).format('YYYY-MM-DD HH:mm:ssZ')
    const uuidv4 = require('uuid/v4')
    const recurring_uuid = uuidv4()
    if (this.rrule_array.length > 0) {
      this.rrule_array.forEach(item => {
        const e: any = {
          start_time: item.start,
          end_time: item.end,
          citizen_name: this.user_name,
          contact_information: this.user_contact_info,
          blackout_flag: 'Y',
          recurring_uuid: recurring_uuid
        }
        if (this.notes) {
          e.comments = this.notes
        }
        this.postAppointment(e)
        this.getAppointments()
      })
    } else if (this.rrule_array.length === 0) {
      const e: any = {
        start_time: start_date,
        end_time: end_date,
        citizen_name: this.user_name,
        contact_information: this.user_contact_info,
        blackout_flag: 'Y'
      }
      if (this.notes) {
        e.comments = this.notes
      }

      this.postAppointment(e)
      this.getAppointments()
    }

    this.recurring_blackout_boolean = true
    this.single_blackout_boolean = true
    this.getAppointments()
    this.toggleAppointmentBlackoutModal(false)
    this.rrule_text = ''
    this.rrule_array = []
    this.recurring_input_state = ''
    this.single_input_boolean = ''
  }

  formatStartDate (date) {
    const formatted_start_date = moment(date).format('YYYY-MM-DD HH:mm')
    return formatted_start_date
  }

  formatEndDate (date) {
    const formatted_end_date = moment(date).format('HH:mm')
    return formatted_end_date
  }

  generateRule () {
    this.hideCollapse('collapse-event-selection')
    this.hideCollapse('collapse-recurring-events')
    this.recurring_blackout_boolean = true
    this.single_blackout_boolean = true
    this.next_boolean = false
    const start_year = parseInt(moment(this.recurring_start_date).utc().clone().format('YYYY'))
    const start_month = parseInt(moment(this.recurring_start_date).utc().clone().format('MM'))
    const start_day = parseInt(moment(this.recurring_start_date).utc().clone().format('DD'))
    const start_hour = parseInt(moment(this.recurring_start_time).utc().clone().format('HH'))
    const local_start_hour = parseInt(moment(this.recurring_start_time).clone().format('HH'))
    const start_minute = parseInt(moment(this.recurring_start_time).utc().clone().format('mm'))
    const end_year = parseInt(moment(this.recurring_end_date).utc().clone().format('YYYY'))
    const end_month = parseInt(moment(this.recurring_end_date).utc().clone().format('MM'))
    const end_day = parseInt(moment(this.recurring_end_date).utc().clone().format('DD'))
    const end_hour = parseInt(moment(this.recurring_end_time).utc().clone().format('HH'))
    const end_minute = parseInt(moment(this.recurring_end_time).utc().clone().format('mm'))
    const duration = moment.duration(moment(this.recurring_end_time).diff(moment(this.recurring_start_time)))
    const duration_minutes = duration.asMinutes()
    let input_frequency: any = null
    let end_adj_day: any = null
    const local_dates_array: any = []

    switch (this.selected_frequency[0]) {
      case 0:
        input_frequency = RRule.YEARLY
        break
      case 1:
        input_frequency = RRule.MONTHLY
        break
      case 2:
        input_frequency = RRule.WEEKLY
        break
      case 3:
        input_frequency = RRule.DAILY
        break
    }

    if (isNaN(start_year) == false || isNaN(end_year) == false) {
      // TODO Might be Deprecated -- IF RRule Breaks, this is where it will happen
      // TODO remove tzid from rule object
      // INC0048019 - fix UTC error by creating new end day and if end_hour is 4pm PACIFIC (16:00) or later then add 1 day to end of series   ozamani 12/17/2020
      if (start_hour > 15 && end_hour < 8) {
        end_adj_day = end_day + 1
      } else {
        end_adj_day = end_day
      }
      const date_start = new Date(Date.UTC(start_year, start_month - 1, start_day, start_hour, start_minute))
      const until = new Date(Date.UTC(end_year, end_month - 1, end_adj_day, end_hour, end_minute))

      const rule = new RRule({
        freq: input_frequency,
        count: this.selected_count,
        byweekday: this.selected_weekdays,
        dtstart: date_start,
        until: until,
        tzid: Intl.DateTimeFormat().resolvedOptions().timeZone
      })
      const array = rule.all()
      this.rrule_text = rule.toText()
      array.forEach(date => {
         // INC0048019 - fix UTC error by creating new date field and if local time is 4pm PACIFIC (16:00) or later then add 1 day to series   ozamani 12/17/2020
        const adj_date = moment(date)
         if (local_start_hour >= 16 && start_hour == 0) {
          adj_date.add(1, 'day')
        }
        const formatted_start_date = moment(adj_date).clone().set({ hour: local_start_hour }).format('YYYY-MM-DD HH:mm:ssZ')
        const formatted_end_date = moment(adj_date).clone().set({ hour: local_start_hour }).add(duration_minutes, 'minutes').format('YYYY-MM-DD HH:mm:ssZ')
        local_dates_array.push({ start: formatted_start_date, end: formatted_end_date })
      })
    }
    this.rrule_array = local_dates_array
    this.selected_count = ''
    this.selected_weekdays = []
    this.selected_frequency = []
    this.recurring_start_date = ''
    this.recurring_start_time = ''
    this.recurring_end_date = ''
    this.recurring_end_time = ''
    this.recurring_input_boolean = true
    this.recurring_input_state = 'audit_information'
    this.hideCollapse('collapse-blackout-notes')
    this.showCollapse('collapse-information-audit')
  }

  setSingle () {
    this.single_blackout_boolean = !this.single_blackout_boolean
    this.single_input_boolean = false
    this.recurring_input_boolean = false
    this.blackout_date = null
    this.start_time = null
    this.end_time = null
    this.recurring_input_state = ''
    this.single_input_state = ''
    this.hideCollapse('collapse-single-event')
  }

  setRecurring () {
    this.recurring_blackout_boolean = !this.recurring_blackout_boolean
    this.single_input_boolean = false
    this.recurring_input_boolean = false
    this.selected_count = ''
    this.selected_weekdays = []
    this.selected_frequency = []
    this.recurring_start_date = null
    this.recurring_start_time = null
    this.recurring_end_date = null
    this.recurring_end_time = null
    this.recurring_input_state = ''
    this.single_input_state = ''
    this.hideCollapse('collapse-recurring-events')
  }

  checkRecurringInput () {
    if (this.selected_frequency.length > 0 &&
      this.recurring_start_date !== null && this.recurring_start_time !== null && this.recurring_end_date !== null &&
      this.recurring_end_time !== null) {
      this.recurring_input_boolean = true
      this.next_boolean = true
      this.recurring_input_state = 'event_information'
    } else {
      this.recurring_input_boolean = false
    }
  }

  checkSingleInput () {
    if (this.blackout_date !== '' && this.start_time !== '' && this.end_time) {
      this.single_input_boolean = true
      this.single_input_state = 'event_information'
    } else {
      this.single_input_boolean = false
      this.single_input_state = ''
    }
  }

  nextSingleNotes () {
    this.hideCollapse('collapse-event-selection')
    this.hideCollapse('collapse-single-event')
    this.showCollapse('collapse-blackout-notes')
    this.single_input_state = 'notes'
  }

  nextRecurringNotes () {
    this.hideCollapse('collapse-information-audit')
    this.showCollapse('collapse-blackout-notes')
    this.recurring_input_boolean = true
    this.recurring_input_state = 'notes'
  }

  created () {
    this.user_name = 'BLACKOUT PERIOD'
    this.user_contact_info = this.$store.state.user.username
  }

  mounted () {
  }
}
</script>

<style scoped>
.list-group {
  max-height: 75px;
  min-height: 50px;
  overflow-y: scroll;
}
</style>
