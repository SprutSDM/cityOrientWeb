<template>
    <div>
        <v-row>
            <v-col cols="12"
                   sm="6"
                   md="4"
                   lg="3"
                   xl="2"
                   v-for="(quest, index) in quests"
                   :key="index">
                <quest-card :quest="quest"/>
            </v-col>
        </v-row>
        <v-btn class="accent"
               @click="createNewQuest()"
               dark
               fixed
               bottom
               right
               fab>
            <v-icon>mdi-plus</v-icon>
        </v-btn>
    </div>
</template>

<script>
    import QuestCard from "./QuestCard";
    import {httpClient} from "../../api/httpClient";

    export default {
        name: "quests",
        data() {
            return {
                quests: []
            }
        },
        components: {
            QuestCard
        },
        methods: {
            createNewQuest() {
                this.$router.push({name: 'createQuest'})
            }
        },
        mounted() {
            httpClient.get('/quests')
                .then((response) => {
                    this.quests = response.data
                })
                .catch((error) => {
                    console.log("quests load error " + JSON.stringify(error));
                })
        }
    }
</script>
