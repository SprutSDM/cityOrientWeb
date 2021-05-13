import '@mdi/font/css/materialdesignicons.css'
import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import 'vuetify/dist/vuetify.min.css'
import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify);

const vuetify = new Vuetify({
    theme: {
        themes: {
            light: {
                primary: colors.teal,
                accent: colors.indigo.accent4,
                background: colors.grey.lighten3
            }
        }
    },
    icons: {
        iconfont: 'mdi', // default - only for display purposes
    },
})

export default vuetify
