<template>
  <v-container>
    <v-row>
      <!-- Card 1 -->
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-title>General Counts</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12">
                <v-list>
                  <v-list-item v-for="count in counts" :key="count.name">
                    <v-list-item-content>
                      <v-list-item-title>{{ count.name }}</v-list-item-title>
                      <v-list-item-subtitle>{{ count.count }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Card 2 -->
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-title>Maximum Count Object</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12">
                <v-list>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>{{ maxCountObject.name }}</v-list-item-title>
                      <v-list-item-subtitle>{{ maxCountObject.count }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Graph 1 -->
      <v-col cols="12">
        <v-card>
          <v-card-title>Graph 1</v-card-title>
          <v-card-text>
            <!-- Content for Graph 1 -->
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Graph 2 -->
      <v-col cols="12">
        <v-card>
          <v-card-title>Graph 2</v-card-title>
          <v-card-text>
            <!-- Content for Graph 2 -->
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      counts: [],
      maxCountObject: {
        name: '',
        count: 0,
      },
    };
  },
  async created() {
    const response = await axios.get('/api/');
    this.counts = response.data;

    const maxCountResponse = await axios.get('/api/max-count-object/');
    this.maxCountObject = maxCountResponse.data;
  },
};
</script>

<style>
/* Add your custom styles here */
</style>
