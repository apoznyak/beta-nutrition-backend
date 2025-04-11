// Beta Nutrition App - React Native Full Version
import React, { useState } from 'react';
import { View, Text, TextInput, Button, ScrollView, StyleSheet, TouchableOpacity } from 'react-native';

const foodCategories = [
  {
    name: 'Sugary Drinks',
    emoji: '🥤',
    description: 'Includes sodas, juice, sports drinks. High in sugar and acidic.',
    risk: 3,
  },
  {
    name: 'Sticky Snacks',
    emoji: '🍬',
    description: 'Candy, dried fruit, or anything that clings to teeth and is sugar-laden.',
    risk: 3,
  },
  {
    name: 'Refined Carbs',
    emoji: '🍞',
    description: 'Crackers, white bread, chips – break down into sugars quickly.',
    risk: 2,
  },
  {
    name: 'Fruits & Veggies',
    emoji: '🍎',
    description: 'Whole fruits and vegetables are better for teeth and increase saliva flow.',
    risk: -1,
  },
  {
    name: 'Protective Foods',
    emoji: '🧀',
    description: 'Cheese, nuts, and milk help buffer acid and remineralize enamel.',
    risk: -2,
  },
];

const riskTips = {
  'High Risk': 'Limit sugary snacks and drinks. Try to eat more protective foods like cheese and nuts. Brush after meals.',
  'Moderate Risk': 'You're doing okay! Consider swapping some snacks for fruits or veggies and drink more water.',
  'Low Risk': 'Great job! Keep up the balanced diet and maintain good oral hygiene.',
};

export default function App() {
  const [input, setInput] = useState('');
  const [riskScore, setRiskScore] = useState(null);
  const [showCategories, setShowCategories] = useState(false);

  const calculateRisk = () => {
    const foods = input.toLowerCase().split(/,|\n|\s+/).filter(Boolean);
    let score = 0;
    foods.forEach(food => {
      foodCategories.forEach(category => {
        if (food.includes(category.name.toLowerCase().split(' ')[0])) {
          score += category.risk;
        }
      });
    });
    setRiskScore(score);
  };

  const getRiskLevel = (score) => {
    if (score >= 4) return 'High Risk';
    if (score >= 1) return 'Moderate Risk';
    return 'Low Risk';
  };

  const riskLevel = riskScore !== null ? getRiskLevel(riskScore) : null;

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Beta Nutrition</Text>

      <Text style={styles.label}>Enter Foods Consumed:</Text>
      <TextInput
        placeholder="e.g., Juice, Crackers, Fruit"
        value={input}
        onChangeText={setInput}
        style={styles.input}
        multiline
      />
      <Button title="Calculate Risk" onPress={calculateRisk} />

      <TouchableOpacity onPress={() => setShowCategories(!showCategories)}>
        <Text style={styles.toggle}>{showCategories ? 'Hide Food Categories' : 'Show Food Categories'}</Text>
      </TouchableOpacity>

      {showCategories && (
        <>
          <Text style={styles.subTitle}>Food Categories:</Text>
          {foodCategories.map((category, index) => (
            <Text key={index} style={styles.category}>
              {category.emoji} <Text style={{ fontWeight: 'bold' }}>{category.name}:</Text> {category.description}
            </Text>
          ))}
        </>
      )}

      <Text style={styles.subTitle}>Result:</Text>
      <Text style={styles.result}>
        {riskLevel ? `${riskLevel} (${riskScore})` : 'Your caries risk level will be shown here based on the foods entered.'}
      </Text>

      {riskLevel && (
        <Text style={styles.tip}>
          💡 <Text style={{ fontWeight: 'bold' }}>Tip:</Text> {riskTips[riskLevel]}
        </Text>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  label: {
    fontSize: 18,
    marginTop: 20,
  },
  input: {
    borderWidth: 1,
    padding: 10,
    marginVertical: 10,
    borderRadius: 5,
    minHeight: 60,
  },
  toggle: {
    fontSize: 16,
    color: 'blue',
    marginTop: 15,
    textAlign: 'center',
  },
  subTitle: {
    fontSize: 18,
    marginTop: 30,
    marginBottom: 10,
  },
  category: {
    marginBottom: 10,
  },
  result: {
    fontSize: 16,
    color: 'gray',
    marginTop: 10,
  },
  tip: {
    fontSize: 16,
    color: '#333',
    marginTop: 20,
    backgroundColor: '#eef9f2',
    padding: 10,
    borderRadius: 6,
  },
});


