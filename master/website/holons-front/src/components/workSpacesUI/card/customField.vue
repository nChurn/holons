<template lang="html">
<div>
    <p><label :for="name">{{field.name}}:</label></p>
    <textarea-autosize
        v-if="field.type === 'multiline' || field.type === 'richtext'"
        v-model="value"
        rows="1"
        placeholder="..."
        class="task-list__input"
        :onblur="saveField(field.id, value)"
        @keyup.enter="$event.target.blur()"
        :id="name"
    />
    <input
        v-else-if="field.type !== 'dropdown'"
        v-model="value"
        placeholder="..."
        class="task-list__input"
        @blur="saveField(field.id, value)"
        @keyup.enter="$event.target.blur()"
        :type="field.type"
        :id="name"
    />
    <select
        v-else-if="field.type === 'dropdown'"
        v-model="value"
        class="task-list__input"
        @blur="saveField(field.id, value)"
        @keyup.enter="$event.target.blur()"
        :type="field.type"
        :id="name"
    >
    <option
        v-for="option in field.extra"
        :value="option"
        :key="option"
    >
        {{option}}
    </option>
    </select>
</div>
</template>

<script>

export default {
    name: 'CustomField',

    props: {
        field: {
            type: Object,
            default: () => {}
        },
        saveField: {
            type: Function,
            default: () => {}
        },
        value: {
            type: String,
            default: ""
        }
    },

    data() {
        return {
            name: '__cf' + this.field.id
        }
    },
}
</script>

<style scoped lang="css">

</style>
