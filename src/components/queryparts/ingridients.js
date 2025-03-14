import React, { useState } from 'react';
import { TextField, Box, Typography, Button, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import '../../css/IngredientSelection.css';
import SearchIcon from '@mui/icons-material/Search';
import { BorderLinearProgress } from './progressbar';

const IngredientSelection = ({ handleGenerateRecipies, backToCuisine, chosenIngredients, setChosenIngredients }) => {


	const [ingredient, setIngredient] = useState('');

	const handleIngredientChange = (e) => {
		setIngredient(e.target.value);
	};

	const handleAddIngredient = () => {
		if (ingredient && !chosenIngredients.includes(ingredient)) {
			setChosenIngredients((prev) => [...prev, ingredient]);
			setIngredient(''); // Clear input field
		}
	};

	// Handler to remove an ingredient
	const handleRemoveIngredient = (removeIndex) => {
		setChosenIngredients((prev) => prev.filter((_, index) => index !== removeIndex));
	};

	return (
		<div className="ingredient-container">
			<div>
				<Typography variant="h5" className="header">
					Which ingredients would you like to include?
				</Typography>
			</div>
			
			<Box sx={{ width: '100%' }} className="progress-bar-ingr">
    			<BorderLinearProgress color="success" variant="determinate" value={80} />
			</Box>

			<Box className="input-container">
				<TextField
					label="Type ingredient"
					value={ingredient}
					onChange={handleIngredientChange}
					variant="outlined"
					className="ingredient-input"
					onKeyDown={(e) => {
						if (e.key === 'Enter') {
							handleAddIngredient();
						}
					}}
				/>
				<Button
					variant="contained"
					color="primary"
					className="add-btn"
					onClick={handleAddIngredient}
				>
					Add
				</Button>
			</Box>

			<Box className="chosen-container">
				<Typography variant="body1" className="chosen-header">
					Chosen ingredients:
				</Typography>
				<div className="chosen-list">
					{chosenIngredients.map((ingredient, index) => (
						<div key={index} className="chosen-item">
							{ingredient}
							<IconButton
								size="small"
								color="error"
								onClick={() => handleRemoveIngredient(index)}
								className="remove-btn"
							>
								<CloseIcon />
							</IconButton>
						</div>
					))}
				</div>
			</Box>

			<Box className="button-container">
				<Button variant="contained" color="error" className="prev-btn" onClick={() => backToCuisine()}>
					Back
				</Button>
				<Button variant="contained" color="success" className="find-btn" endIcon={<SearchIcon />} onClick={() => handleGenerateRecipies()}>
					Find
				</Button>
			</Box>
		</div>
	);
};

export default IngredientSelection;
