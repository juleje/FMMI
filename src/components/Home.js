import React, { useContext, useEffect, useState } from "react";
import { PreferenceContext } from "../contexts/PreferenceContext";
import "../css/Home.css";
import {
  Checkbox,
  FormControlLabel,
  Button,
  Typography,
  Box,
} from "@mui/material";
import homebanner from "../img/salad.jpg";
//import minimalist from '../img/minimalist-logo.jpg'
import { useNavigate } from "react-router-dom";

const Home = () => {
  const state = useContext(PreferenceContext);
  console.log(state.preference);

  const navigate = useNavigate();

  return (
    <div className="container">
      {/* Header */}
      <h1 className="home-header">Bright Bites</h1>
      {/* image */}
      <div className="box">
        <img src={homebanner} alt="Healthy person" className="healthy-image" />

        <Box className="home-checkbox-container">
          <FormControlLabel
            control={
              <Checkbox
                checked={state.preference}
                onChange={() => state.setPreference(!state.preference)}
              />
            }
            label="Add Healthiness Explanations"
          />
        </Box>

        {/* Start Button */}
        <button className="start-button" onClick={() => navigate("/query")}>
          START
        </button>
      </div>
      {/* Description */}
      <p className="description">
        The recipe recommendation app designed to inspire your healthy
        lifestyle!
      </p>
    </div>
  );
};

export default Home;
